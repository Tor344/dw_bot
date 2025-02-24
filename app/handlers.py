import os
import shutil
from aiogram import Router, F,Bot
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards as kb
import app.download_video as down
import app.sqlite as db

router = Router()

class admi(StatesGroup):
    admin = State()
    append = State()
    delit = State()

@router.message(Command('start'))
async def start(message: Message,bot:Bot):
    await db.add_user_if_not_exists(message.from_user.id)


    await message.answer(""""Привет, я быстро скачиваю видео из Instagram, YouTube Shorts и Pinterest. Для скачивания отправьте ссылку на видео: 🔻" """)


@router.message(Command("Consol"))
async def cosol(message:Message,state:FSMContext):
    await state.set_state(admi.admin)
    await message.answer("Вы вошли в консоль админа", reply_markup=kb.keyboard)

@router.message(F.text == "Список пользователей",admi.admin)
async def list_p(message:Message):
    quntt = await db.get_user_count()
    await message.answer(str(quntt))


@router.message(F.text == "Добавить канал",admi.admin)
async def list_p(message:Message,state:FSMContext):
    await state.set_state(admi.append)
    await message.answer("Напишите имя канала")


@router.message(admi.append)
async def list_p(message:Message,state:FSMContext):
    flag = await db.add_channel(message.text)
    if flag == True:
        await message.answer("Канал был добавлен")
    else:
        await message.answer("Канал уже есть")
    await state.set_state(admi.admin)


@router.message(F.text == "Убрать канал",admi.admin)
async def list_p(message:Message,state:FSMContext):
    await state.set_state(admi.delit)
    chen = await db.get_all_channels()
    text = "Какой вы собираеттесь удалить канал?\n"
    for i in range(len(chen)):
        text += f"Канал {i+1}: {chen[i]}\n"
    await message.answer(text)

@router.message(admi.delit)
async def list_p(message:Message,state:FSMContext):
    flag = await db.delete_channel(message.text)
    if flag == True:
        await message.answer("Канал удалился")

    else:
        await message.answer("Неверное имя канала")
    await state.set_state(admi.admin)


@router.message(F.text == "Выход",admi.admin)
async def list_p(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("Вывышли из консоли разработчика",reply_markup=kb.delit)


@router.message(F.text)
async def set_url(message:Message,bot:Bot):
    flag = 0
    channels = await db.get_all_channels()
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=f"@{channel}", user_id=message.from_user.id)
            if member.status in ["member", "administrator", "creator"]:
                pass
            else:
                await message.answer("Подпишитесть на канал для использования бота",reply_markup=kb.create_subscription_keyboard(channels))
                flag = 1
                break
        except Exception as e:

            print(f"Ошибка при проверке канала {channel}: {e}")
            flag = 1
            break
    if flag == 0:
        try:
            exzam = await down.check_links(message.text)
            if exzam == "instagram":
                await message.answer("Видео скоро скачается")
                video_path = await down.download_video(message.text, "1350p")
                async with ChatActionSender.upload_video(chat_id=message.from_user.id, bot=bot):
                    video = FSInputFile(video_path)
                    await bot.send_video(message.from_user.id, video=video, caption=message.text)

                # Удаляем оригинальный и сжатый файлы
                if os.path.exists(video_path):
                    os.remove(video_path)

            elif exzam in ["youtube_shorts","pinterest"]:
                await message.answer("Видео скоро скачается")
                video_path = await down.download_video(message.text, "720p")
                async with ChatActionSender.upload_video(chat_id=message.from_user.id, bot=bot):
                    video = FSInputFile(video_path)
                    await bot.send_video(message.from_user.id, video=video,caption=message.text)

                # Удаляем оригинальный и сжатый файлы
                if os.path.exists(video_path):
                    os.remove(video_path)
            else:
                await message.answer(f"Извините, но '{message.text}' не соответствует релевантной ссылке. Попробуйте еще раз...")
        except Exception as e:
            print(f"Извините, при скачивании произошла ошибка: {str(e)}")
            await message.answer("Извините, при скачевании произошла ошибка")
            shutil.rmtree("/home/dw_bot/video")

