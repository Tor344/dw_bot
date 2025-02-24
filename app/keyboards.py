from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_subscription_keyboard(channels):
    """
    Создает инлайн-клавиатуру с кнопками для подписки на каналы.
    :param channels: Список имен каналов (или ссылок на них).
    :return: InlineKeyboardMarkup
    """
    print(channels)
    builder = InlineKeyboardBuilder()
    for channel in channels:

        # Создаем кнопку с текстом "Подписаться на <имя канала>"
        builder.add(InlineKeyboardButton(
            text=f"Подписаться",
            url=f"https://t.me/{channel}"
        ))
        # Располагаем кнопки в один столбец
        builder.adjust(1)
        return builder.as_markup()



keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Список пользователей")],  # Первая строка с одной кнопкой
        [KeyboardButton(text="Добавить канал")],        # Вторая строка с одной кнопкой
        [KeyboardButton(text="Убрать канал")],          # Третья строка с одной кнопкой
        [KeyboardButton(text="Выход")]                 # Четвертая строка с одной кнопкой
    ],
    resize_keyboard=True  # Опционально: автоматически изменять размер клавиатуры
)



delit = ReplyKeyboardRemove()



