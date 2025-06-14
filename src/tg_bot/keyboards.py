from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline_keyboard(width, *args, **kwargs):
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(text=button,
                                     callback_data=button)
            )

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                InlineKeyboardButton(text=text,
                                     callback_data=button)
            )

    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup()