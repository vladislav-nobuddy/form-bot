import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
logging.basicConfig(level=logging.INFO)
from time import sleep
import datetime
from handlers import anketa

dp = Dispatcher()
bot = Bot(token='ВСТАВЬТЕ СЮДА ВАШ ТОКЕН')


@dp.message(Command("start"))
@dp.message(lambda message: message.text == "start")
async def cmd_start(message: Message):
    await message.answer('Привет! С помощью этого бота ты можешь вступить в нашу тиму!👋', reply_markup=ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text='🚩Начать!🚩', resize_keyboard=True)
            ]
        ]
    ))



async def main():
    dp.include_routers(anketa.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())