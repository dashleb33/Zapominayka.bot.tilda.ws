from Keyboards import *
from work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, executor, types
from handlers.FSM import *
from create_bot import bot
from handlers import global_variables as gv

# ПРИСТУПИТЬ К ТРЕНИРОВКЕ
# @dp.callback_query_handler(text='newtrain1')
async def new_train(callback: types.CallbackQuery):
    id_1 = callback.message.chat.id
    await add_user_and_date_in_base(id_1)
    if gv.chosen_theme:
        flag = True  # тема выбрана - печатаем с текстом "сгенерированы вопросы по теме"
        gv.question_formulate = await take_question_formulate(gv.chosen_theme)
    else:
        gv.chosen_theme = 'страна-столица'
        gv.question_formulate = await take_question_formulate(gv.chosen_theme)
        flag = False
    gv.dict_ques_answ = await select_questions_for_theme(gv.chosen_theme)
    if flag:
        await callback.message.answer(emojis.encode(f'Сгененированы вопросы по теме "{gv.chosen_theme}"\n'))
    else:
        await callback.message.answer(emojis.encode(f'Тема не выбрана, сгененированы вопросы '
                                                    f'по теме "страна-столица" \n'))
    global right_answer
    global question
    global question_id
    global photo
    play_tuple = gv.dict_ques_answ.pop()
    print(play_tuple)
    gv.question_id = play_tuple[0]
    gv.question = play_tuple[1]
    gv.right_answer = play_tuple[2]
    gv.photo = play_tuple[3]
    if gv.chosen_theme not in ['флаг-страна', 'архитектура, понятия']:
        await callback.message.answer(emojis.encode(f'{gv.question_formulate} "{gv.question}"?  \n \n'
                                                    ),reply_markup=cancel_kb)
    else:
        print(gv.question)
        if gv.photo:
            await bot.send_photo(chat_id=callback.message.chat.id, photo=gv.photo)
        await callback.message.answer((f'{gv.question_formulate} {gv.question}'), reply_markup=cancel_kb)
    await Form.play_1.set()
    await callback.answer()



# НАЧАТЬ
# @dp.callback_query_handler(text='go1')
async def tutorial_guide(callback: types.CallbackQuery):
    global right_answer
    global question
    global question_id
    if gv.dict_ques_answ:
        play_tuple = gv.dict_ques_answ.pop()
        print(play_tuple)
        gv.question_id = play_tuple[0]
        gv.question = play_tuple[1]
        gv.right_answer = play_tuple[2]
        gv.photo = play_tuple[3]
        if gv.chosen_theme not in ['флаг-страна', 'архитектура, понятия']:
            await callback.message.answer(emojis.encode(f'{gv.question_formulate} "{gv.question}"?  \n \n'
                                                        ),reply_markup=cancel_kb)
        else:
            print(gv.question)
            if gv.photo:
                await bot.send_photo(chat_id=callback.message.chat.id, photo=gv.photo)
            await callback.message.answer((f'{gv.question_formulate}'), reply_markup=cancel_kb)
        await Form.play_1.set()
        await callback.answer()
    else:
        await bot.send_message(callback.message.chat.id,
                               text=f'Вы ответили на все вопросы! \n Можете начать сначала из главного меню', reply_markup=cancel_kb)


# раздел "игра", проверка ответа
# @dp.message_handler(state=Form.play_1)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    us_id = message.from_user.id
    gv.us_id = us_id
    if answer.lower() == gv.right_answer.lower():
        await message.reply(emojis.encode(f'Верно! \n'
                                          f' \n'
                                          f'{gv.question_formulate} "{gv.question}"? \n'
                                          ), reply_markup=correct_kb)
        await add_question_to_base(us_id, gv.question_id, 1, gv.chosen_theme, quantity_answers=1)
        await state.finish()
    else:
        global user_rule_from_base
        user_rule_from_base = await show_my_rule(us_id, gv.question_id)
        print(user_rule_from_base)
        if user_rule_from_base:
            print('it not empty')
            keyboard = un_correct_ans_kb_yesrule
        else:
            print('it empty')
            keyboard = un_correct_ans_kb_norule
        print(keyboard)
        await message.reply(emojis.encode('Неправильно :red_circle: \n'
                                          'Попробуйте ещё раз \n'
                                          ), reply_markup=keyboard)


# @dp.callback_query_handler(text='hint_btn', state=Form.play_1)
async def hint_call(callback: types.CallbackQuery, state: FSMContext):
    print(user_rule_from_base)
    if user_rule_from_base:
        if gv.chosen_theme not in ['флаг-страна', 'архитектура, понятия']:
            await callback.message.reply(
                f'Ваше мнемоническое правило для {gv.question_formulate} "{gv.question}"? "{user_rule_from_base}", попробуйте отгадать ещё раз\n'
                f'', reply_markup=un_correct_max_kb)
        else:
            if gv.photo:
                await bot.send_photo(callback.message.chat.id, photo=gv.photo,
                                    caption=f'Ваше мнемоническое правило "{user_rule_from_base}", попробуйте отгадать ещё раз\n '
                                         ,reply_markup=un_correct_max_kb)
            else:
                await bot.send_message(callback.message.chat.id,
                                     text=f'Ваше мнемоническое правило "{user_rule_from_base}", попробуйте отгадать ещё раз\n '
                                     ,reply_markup=un_correct_max_kb)
    else:
        if gv.chosen_theme not in ['флаг-страна', 'архитектура, понятия']:
            await callback.message.reply(
                f'У вас нет мнемонического правила для "вопроса {gv.question_formulate} "{gv.question}"?", попробуйте отгадать ещё раз \n'
                , reply_markup=un_correct_max_kb)
        else:
            await bot.send_photo(callback.message.chat.id, photo=gv.photo,
                                 caption="У вас нет мнемонического правила для этого вопроса"
                                         " попробуйте отгадать ещё раз",
                                 reply_markup=un_correct_max_kb)
    await callback.answer()


# @dp.callback_query_handler(text='hint_max_btn', state=Form.play_1)
async def answer_check(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.reply(emojis.encode(f'Ответ: {gv.right_answer} \n'
                                               ), reply_markup=correct_kb)
    await add_question_to_base(gv.us_id, gv.question_id, 0, gv.chosen_theme, quantity_answers=1)
    await callback.answer()


def register_handlers_exam_train(dp: Dispatcher):
    dp.register_callback_query_handler(new_train, state='*', text='newtrain_1')
    dp.register_callback_query_handler(tutorial_guide, state='*', text='go1')
    dp.register_message_handler(asking, state=Form.play_1)
    dp.register_callback_query_handler(hint_call, state=Form.play_1, text='hint_btn')
    dp.register_callback_query_handler(answer_check, state='*', text='hint_max_btn')