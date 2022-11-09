from Keyboards import *
from work_with_base import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext

#@dp.callback_query_handler(state='*', text='cancel1')
async def cancel_call(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer("Вы вышли из режима, список доступных команд\n"
                                  "Техники - для просмотра техник \n"
                                  "Темы - для выбора темы запоминания\n"
                                  "Начать - чтобы начать заниматься",
                                  reply_markup=inline_kb)
    await callback.answer()

def register_handlers_cancel(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_call, state='*', text='cancel1')