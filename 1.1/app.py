from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import random as r
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config

bot = Bot(token="5752954362:AAE0_BaG6xe8Vc_4OFIYLsTZpUzQjgiB0DI")
storage = MemoryStorage()
dp = Dispatcher(bot)



conn = sqlite3.connect('Base.db', check_same_thread=False)
europe = sqlite3.connect('europe_capitals.db', check_same_thread=False)
cursor = conn.cursor()
cursor_db = europe.cursor()

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
                            " для столиц стран, которые помогут вам обучиться")
        lst = list(range(1, 11))
        r.shuffle(lst)
        for i in lst:
            cursor_db.execute(f'SELECT * FROM capitals WHERE  ID = {i}')
            data = cursor_db.fetchone()
            if data is None:
                continue
            else:
                await message.reply(f'Страна: {data[1]} \n Cтолица: {data[2]} \n Мнемоническое правило: {data[3]}')

@dp.message_handler(commands=['play'])
async def tutorial_guide(message: types.Message):
    await message.reply("Начнем игру, предлагаем вам в процессе создавать свои мнемонические правила")

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
