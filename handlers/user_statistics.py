from Keyboards import *
from work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from handlers.FSM import *
from create_bot import bot
from handlers import global_variables as gv



#@dp.callback_query_handler(text='statistics_btn')
async def statistics_btn_menu(callback: types.CallbackQuery):
    await bot.send_message(chat_id= callback.message.chat.id,
                           text=emojis.encode(
                               "Выберите, какую статистику получить"),
                           reply_markup=kb_startistics)
    await Form.user_statistics.set()

#выбор темы
async def statistics_chose_theme(message: types.Message, state: FSMContext):
    await message.reply(emojis.encode(f'Выберите тему '), reply_markup=kb_subjects)
    await Form.user_statistics2.set()



#Вывод статы по теме
#@dp.callback_query_handler(state ='user_statistics2')
async def statistics_theme(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    gv.us_id = message.from_user.id
    right_answers = await get_statistics_right_answers(gv.us_id, answer)
    all_answers = await get_statistics_all_answers(gv.us_id, answer)
    all_questions = await get_statistics_get_all_questions(gv.us_id, answer)
    usvoenie_temi = round(right_answers*100/all_questions, 2)
    otv_na_vopr = round(right_answers*100/all_questions, 2)
    await bot.send_message(chat_id= message.from_user.id,
                           text=f'Процент усвоения темы {usvoenie_temi}% \n'
                                f'Количество ответов(с верностью более 50%) {right_answers} из {all_answers} отвеченных \n'
                                f'Всего дано ответов на {all_answers} из {all_questions} содержащихся в базе вопросов')






def register_handlers_user_stat(dp: Dispatcher):
    dp.register_callback_query_handler(statistics_btn_menu, state = '*', text='statistics_btn')
    dp.register_message_handler(statistics_chose_theme, state=Form.user_statistics)
    dp.register_message_handler(statistics_theme, state=Form.user_statistics2)


