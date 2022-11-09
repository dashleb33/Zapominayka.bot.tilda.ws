from Keyboards import *
from work_with_base import *
from aiogram import Bot, Dispatcher, executor, types
from handlers import global_variables as gv

#@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    gv.us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    await save_user_in_base(gv.us_id, us_name, us_sname, username)
    await message.reply(emojis.encode("Привет :wave:\n Выберите, пожалуйста, меню: \n"),
                                        reply_markup=inline_kb)


# ВЫЗОВ МЕНЮ
#@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    gv.us_id = message.from_user.id
    await message.reply(emojis.encode("Привет :wave:\n Выберите, пожалуйста, меню: \n"
                                          "/subject - выбор темы для изучения \n"
                                          "/technic - техники запоминания \n"
                                          "/exam - начать заниматься"),
                                        reply_markup=inline_kb)

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])