import os
from aiogram import Router, F,Bot
from aiogram.types import Message, CallbackQuery,FSInputFile, InputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

import app.download_video as down
import app.keyboards as kb


router = Router()


@router.message(Command('start'))
async def start(message: Message,state:FSMContext):
    await message.answer("""Привет, я быстро скачиваю видео и аудио из Instagram,  YouTube, Rutube, VKвидео.

Для скачивания отправьте ссылку на видео или аудио: 🔻""")


@router.message(F.text)
async def set_url(message:Message,state:FSMContext,bot:Bot):
    try:
        exzam = await down.check_links(message.text)
        if exzam == "instagram":
            await message.answer("Видео скоро скачается")
            video_path = await down.download_video(message.text, "1350p")
            async with ChatActionSender.upload_video(chat_id=message.from_user.id, bot=bot):
                video = FSInputFile(video_path)  # Используем сжатый файл
                await bot.send_document(message.from_user.id, document=video,caption=message.text)

            # Удаляем оригинальный и сжатый файлы
            if os.path.exists(video_path):
                os.remove(video_path)
        elif exzam in ["youtube","rutube","vk"]:
            await state.update_data(url=message.text)
            await message.answer("Выберите качесто видео",reply_markup=kb.start_format)
        else:
            await message.answer("Видимо ссылка была неправильно введина, попробуте еще раз")
    except Exception as e:
            print(f"Извините, при скачивании произошла ошибка: {str(e)}")
            await message.answer("Извините, при скачевании произошла ошибка")


@router.callback_query(F.data.in_(["144p", "240p", "360p", "480p", "720p", "1080p"]))
async def handle_quality_selection(callback: CallbackQuery,state:FSMContext,bot:Bot):
    try:
        await callback.message.delete()
        await callback.message.answer("Видео скоро скачается")
        data = await state.get_data()
        video_path = await down.download_video(data["url"], callback.data)
        async with ChatActionSender.upload_video(chat_id=callback.from_user.id, bot=bot):
            video = FSInputFile(video_path)
            await bot.send_document(callback.from_user.id, document=video,caption=data["url"])
        if os.path.exists(video_path):
            os.remove(video_path)


    except Exception as e:
        print(f"Извините, при скачивании произошла ошибка: {str(e)}")
        await callback.message.answer("Извините, при скачевании произошла ошибка")
