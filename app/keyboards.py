from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_format = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="144p", callback_data="144p"),
     InlineKeyboardButton(text="240p", callback_data="240p"),
     InlineKeyboardButton(text="360p", callback_data="360p")],
    [InlineKeyboardButton(text="480p", callback_data="480p"),
     InlineKeyboardButton(text="720p", callback_data="720p"),
     InlineKeyboardButton(text="1080p", callback_data="1080p")]
])