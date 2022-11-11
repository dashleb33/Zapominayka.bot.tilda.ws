from Keyboards import *
from aiogram import Dispatcher, types


async def process_exam_menu(callback: types.CallbackQuery):
    await callback.message.answer("Доступны следующие команды: \n"
                                  "Тренировка - для проверки знаний \n"
                                  "Правила - посмотреть свои мнемонические правила",
                                  reply_markup=exam_kb)
    await callback.answer()

def register_handlers_second_menu(dp: Dispatcher):
    dp.register_callback_query_handler(process_exam_menu, state = '*', text='exam_btn')