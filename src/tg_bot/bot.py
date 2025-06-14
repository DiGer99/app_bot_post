import asyncio
from src.config.config import BOT_TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from src.tg_bot.keyboards import create_inline_keyboard
from src.db.requests import get_post_from_header, bind_tg_to_api, get_posts_user, get_user_from_tg_id

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text="Введите код")


@dp.message(F.len() == 6 and F.text.isdigit())
async def code_bind_to_api(message: Message):
    await message.answer(bind_tg_to_api(code=message.text, tg_id=message.from_user.id))


@dp.message(Command("posts"))
async def command_posts_press(message: Message):
    user = get_user_from_tg_id(tg_id=message.from_user.id)
    posts = get_posts_user(user_id=user.id)
    headers = [p.header for p in posts]
    await message.answer(
                text="Ваши посты:",
                reply_markup=create_inline_keyboard(2, *headers)
            )


@dp.callback_query()
async def process_search_post_from_header(callback: CallbackQuery):
    post = get_post_from_header(callback.from_user.id, callback.data)
    await callback.message.answer(text=f"{post.text}\n{post.created_at:%d.%m.%Y %H:%M}")
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
