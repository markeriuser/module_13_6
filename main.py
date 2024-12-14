from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Кнопки для инлайн клавиатуры
kbinline = InlineKeyboardMarkup(row_width=2)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='Calories')
button2 = InlineKeyboardButton(text='Формулы рассчёта', callback_data='formulas')
kbinline.add(button, button2)

# Кнопки базовые
kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb.add(button1, button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    print('привет! Я бот помогающий твоему здоровью.')
    await message.answer("привет! Я бот помогающий твоему здоровью.", reply_markup=kb)

@dp.message_handler(text="Информация")
async def all_message(message: types.Message):
    print("Это бот который помогает твоему здоровью")
    await message.answer("Это бот который помогает твоему здоровью")

@dp.message_handler(text='Рассчитать')
async def start_message(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=kbinline)

@dp.callback_query_handler(text="formulas")
async def get_formulas(call: types.CallbackQuery):
    print("информация о боте")
    await call.message.answer("для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;"
                              "\n \n для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.")
    await call.answer()

# возраст
@dp.callback_query_handler(text="Calories")
async def set_age(call: types.CallbackQuery):
    print("начало вычисления калорий")
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()

# рост
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

# вес
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

# ответ калории
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories1 = 10 * weight + 6.25 * growth - 5 * age + 5
    calories2 = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Ваша норма калорий {calories1} если вы мужчинка и {calories2} если вы женщинка")
    await state.finish()

@dp.message_handler()
async def all_message(message: types.Message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
