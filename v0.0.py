from aiogram import Bot, Dispatcher, executor, types
import sqlite3

bot = Bot(token="5752954362:AAE0_BaG6xe8Vc_4OFIYLsTZpUzQjgiB0DI")
dp = Dispatcher(bot)
conn = sqlite3.connect('Base.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
        await message.reply("Привет!\nЯ твой бот!\nДля регистрации напиши что-нибудь.")


@dp.message_handler()
async def send_welcome(message: types.Message):
    await message.reply('Привет, приступим к регистрации!')
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
    await message.reply('Ваше имя добавлено в базу данных!')


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
