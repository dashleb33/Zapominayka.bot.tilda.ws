from Keyboards import *
from work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from handlers.FSM import *
from create_bot import dp, bot

async def process_exam_menu(callback: types.CallbackQuery):
    await callback.message.answer("Доступны следующие команды: \n"
                                  "Тренировка - для проверки знаний \n"
                                  "Правила - посмотреть своим мнемонические правила",
                                  reply_markup=exam_kb)
    await callback.answer()

def register_handlers_second_menu(dp: Dispatcher):
    dp.register_callback_query_handler(process_exam_menu, state = '*', text='exam_btn')