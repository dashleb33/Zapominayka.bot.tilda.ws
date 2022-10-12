from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import random as r


bot = Bot(token="5752954362:AAE0_BaG6xe8Vc_4OFIYLsTZpUzQjgiB0DI")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('Base.db', check_same_thread=False)
europe = sqlite3.connect('europe_capitals.db', check_same_thread=False)
cursor = conn.cursor()
cursor_db = europe.cursor()
lst = []
class Form(StatesGroup):
    teaching = State()
    ask_eche_primer = State()
    x3 = State()

# добавление пользователя в базу данных
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ твой бот!\n Используйте /help, чтобы узнать список всех команд")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Доступные следующие команды: /r для регистрации , /t для обучения, 'play для игры ")


@dp.message_handler(commands=['r'])
async def process_registration(message: types.Message):
        await message.reply('Приступим к регистрации!\nЭто нужно, чтобы ваши мнемонические правила и пргогресс сохранялись')
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
        await message.reply('Вы добавлены в базу пользователей!')

@dp.message_handler(commands=['t'])
async def tutorial_guide(message: types.Message):
        await message.reply("Давайте приступим к обучению. \n Сейчас мы покажем вам примеры мнемонических правил"
                            " для столиц стран, которые помогут вам обучиться, поставьте +, если готовы")
        global lst
        lst = list(range(1, 11))
        r.shuffle(lst)
        await Form.teaching.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Cancelled.')

@dp.message_handler(state=Form.teaching)
async def show_examples(message: types.Message, state: FSMContext):
    if lst:
        a = lst.pop()
        cursor_db.execute(f'SELECT * FROM capitals WHERE  ID = {a}')
        data = cursor_db.fetchone()
        await message.reply(f'Страна: {data[1]} \n Cтолица: {data[2]} \n Мнемоническое правило: {data[3]}')
        await message.reply(f'Показать ещё пример?')
        await Form.ask_eche_primer.set()

@dp.message_handler(state=Form.ask_eche_primer)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    if answer in ['yes', 'y', 'да', '+']:
        await Form.teaching.set()
    else:
        await message.reply('Выберете другое в меню.')
        await state.finish()

@dp.message_handler(commands=['play'])
async def tutorial_guide(message: types.Message):
    await message.reply("Начнем игру, предлагаем вам в процессе создавать свои мнемонические правила")

@dp.message_handler()
async def process_registration(message: types.Message):
        await message.reply('Пожалуйста, выберете команду из меню, для вызова команд наберите /help')


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
