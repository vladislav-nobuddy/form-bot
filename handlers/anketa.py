import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
import json

bot = Bot(token='ВСТАВЬТЕ СЮДА ВАШ ТОКЕН')

router = Router()
admin = 'ВСТАВЬТЕ СЮДА ВАШ АЙДИ (цифрами)'

class anketa(StatesGroup):
    known_as = State()
    know_mean = State()
    time = State()

@router.message(lambda message: message.text == "🔁Заполнить заново🔁")
@router.message(lambda message: message.text == "🚩Начать!🚩")
async def start_anket(message: Message, state: FSMContext):
    await state.set_state(anketa.known_as)
    await state.update_data(id=message.from_user.username)
    await message.answer('Откуда вы про нас узнали?', reply_markup=ReplyKeyboardRemove())

@router.message(anketa.known_as)
async def know_anket(message: Message, state: FSMContext):
    await state.update_data(known_as=message.text)
    await message.answer('Знакомы с такими понятиями как Антидетект-Браузеры и прокси? \nЕсли да, то в какой сфере работал с ними?')
    await state.set_state(anketa.know_mean)

@router.message(anketa.know_mean)
async def know_mean(message: Message, state:FSMContext):
    await state.update_data(knowledge=message.text)
    await message.answer('Сколько готовы уделять времени работе?')
    await state.set_state(anketa.time)

@router.message(anketa.time)
async def time_(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    user_data = await state.get_data()
    await message.answer(
    f'''
    Ваша анкета: 
    Откуда узнали: {user_data['known_as']}
    Знакомы ли с понятиями: {user_data['knowledge']}
    Сколько готовы уделять времени: {user_data['time']}
    ''', reply_markup=ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text='✅Отправить!✅', resize_keyboard=True),
                KeyboardButton(text='🔁Заполнить заново🔁', resize_keyboard=True)
            ]
        ]
    ))
    await state.clear()

    @router.message(lambda message: message.text == "✅Отправить!✅")
    async def send(message: Message):
        await message.answer('Анкета отправлена!')
        await bot.send_message(admin, f'Новая анкета!')
        await bot.send_message(admin, f'''
    Пользователь: {user_data['id']}
    Откуда узнали: {user_data['known_as']}
    Знакомы ли с понятиями: {user_data['knowledge']}
    Сколько готовы уделять времени: {user_data['time']}
    ''')
