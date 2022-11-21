from Keyboards import *
from work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from handlers.FSM import *
from handlers import global_variables as gv

#@dp.callback_query_handler(text='subject1')
async def show_subjects(callback: types.CallbackQuery):
    global all_themes
    all_themes = await select_all_themes_from_base()
    await callback.message.answer(emojis.encode('Выберите и напишите тему для занятий из предложенных: :arrow_down:'))
    await callback.message.answer('\n'.join(all_themes))
    await Form.chose_theme_btn.set()
    await callback.answer()



async def chose_theme(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer in all_themes:
        gv.chosen_theme = answer
        gv.question_formulate = await take_question_formulate(gv.chosen_theme)
        await message.reply(emojis.encode(f'Тема установлена "{gv.chosen_theme}"\n'
                                          f'Теперь вы можете начать заниматься или изучить техники мнемоники'),
                            reply_markup=inline_kb)
        await state.finish()
    else:
        await message.reply(
            emojis.encode('Данной темы нет в списке, попробуйте ещё раз. \nДля выхода нажмите'),
            reply_markup=cancel_kb)

def register_handlers_subjects(dp: Dispatcher):
    dp.register_message_handler(chose_theme, state = Form.chose_theme_btn)
    dp.register_callback_query_handler(show_subjects, state = '*', text='subject1')
