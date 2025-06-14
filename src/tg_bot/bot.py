import asyncio
from src.config.config import BOT_TOKEN
from aiogram import Bot, Dispatcher, F
import requests
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from src.tg_bot.keyboards import create_inline_keyboard
from src.db.models import Post
from src.db.requests import get_post_from_header, bind_tg_to_api

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text="Введите код")


@dp.message(F.len() == 6 and F.text.isdigit())
async def code_bind_to_api(message: Message):
    await message.answer(bind_tg_to_api(code=message.text, tg_id=message.from_user.id))
    # response = requests.post(
    #     url=f"http://localhost:8000/reg/bind-telegram/",
    #     json={
    #         "code": code,
    #         "tg_id": message.from_user.id
    #     }
    # )
    # if response.status_code == 200:
    #     await message.answer(text="Телеграм успешно привязан")
    # else:
    #     await message.answer(text="Код не найден или уже использован")


@dp.message(Command("posts"))
async def command_posts_press(message: Message):
    response = requests.get(
        url=f"http://localhost:8000/reg/bind-telegram/{message.from_user.id}",
    )
    if response.status_code == 200:
        posts = response.json()
        headers = [post["header"] for post in posts]
        if not posts:
            await message.answer(text="У вас пока нет постов")
        else:
            await message.answer(reply_markup=create_inline_keyboard(2, *headers))
    else:
        await message.answer("Не удалось получить посты")


@dp.callback_query()
async def process_search_post_from_header(callback: CallbackQuery):
    post: Post = get_post_from_header(callback.message.text)
    await callback.answer(text=f"{post.text}\n{post.created_at}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
