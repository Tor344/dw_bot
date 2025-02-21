import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery,FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.download_video as down
import app.keyboards as kb


router = Router()


@router.message(Command('start'))
async def start(message: Message,state:FSMContext):
    await message.answer("""Привет, я быстро скачиваю видео и аудио из Instagram,  YouTube, Rutube, VKвидео.

Для скачивания отправьте ссылку на видео или аудио: 🔻""")


@router.message(F.text)
async def set_url(message:Message,state:FSMContext):
    try:
        exzam = await down.check_links(message.text)
        if exzam == "instagram":
            await message.answer("Видео скоро скачается")
            video_path = await down.download_video(message.text,"1350p")
            video = FSInputFile(video_path)
            await message.answer_video( video=video,caption=message.text,timeout=300)
            if os.path.exists(video_path):
                os.remove(video_path)
        elif exzam in ["youtube","rutube","vk"]:
            await state.update_data(url=message.text)
            await message.answer("Выберите качесто видео",reply_markup=kb.start_format)
        else:
            await message.answer("Видимо ссылка была неправильно введина, попробуте еще раз")
    except:
        await message.answer("Извините, при скачевании произошла ошибка")

@router.callback_query(F.data.in_(["144p", "240p", "360p", "480p", "720p", "1080p"]))
async def handle_quality_selection(callback: CallbackQuery,state:FSMContext):
    try:
        await callback.message.delete()
        await callback.message.answer("Видео скоро скачается")
        data = await state.get_data()
        video_path = await down.download_video(data["url"], callback.data)
        video = FSInputFile(video_path)
        await callback.message.answer_video(video=video,caption=data["url"], timeout=500)
        if os.path.exists(video_path):
            os.remove(video_path)

    except:
        await callback.message.answer("Извините, при скачевании произошла ошибка")
