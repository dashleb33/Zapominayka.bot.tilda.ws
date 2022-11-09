from Keyboards import *
from work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from handlers.FSM import *
from create_bot import dp, bot
from handlers.global_variables import *

# @dp.callback_query_handler(text='exam_btn')
async def process_exam_menu(callback: types.CallbackQuery):
    await callback.message.answer("Доступны следующие команды: \n"
                                  "Тренировка - для проверки знаний \n"
                                  "Правила - посмотреть своим мнемонические правила",
                                  reply_markup=exam_kb)
    await callback.answer()

# ПРИСТУПИТЬ К ТРЕНИРОВКЕ
# @dp.callback_query_handler(text='newtrain1')
async def new_train(callback: types.CallbackQuery):
    global question
    global question_id
    global chosen_theme
    global dict_ques_answ
    if chosen_theme:
        flag = True  # тема выбрана - печатаем с текстом "сгенерированы вопросы по теме"
    else:
        chosen_theme = ('страна-столица')
        flag = False
    dict_ques_answ = await select_questions_for_theme(chosen_theme)
    if flag:
        await callback.message.answer(emojis.encode(f'Сгененированы вопросы по теме "{chosen_theme}"\n'),
                                      reply_markup=go_kb)
    else:
        await callback.message.answer(emojis.encode(f'Тема не выбрана, сгененированы вопросы '
                                                    f'по теме "страна-столица" \n'), reply_markup=go_kb)
    await callback.answer()


# НАЧАТЬ
# @dp.callback_query_handler(text='go1')
async def tutorial_guide(callback: types.CallbackQuery):
    global right_answer
    global question
    global question_id
    play_tuple = dict_ques_answ.pop()
    print(play_tuple)
    question_id = play_tuple[0]
    question = play_tuple[1]
    right_answer = play_tuple[2]
    if chosen_theme != 'флаг-страна':
        await callback.message.answer(emojis.encode(f' "{question}"  \n \n'
                                                    ),reply_markup=cancel_kb)
    else:
        print(question)
        await bot.send_photo(chat_id=callback.message.chat.id, photo=question)
        await callback.message.answer(('текст'), reply_markup=cancel_kb)
    await Form.play_1.set()
    await callback.answer()


# раздел "игра", проверка ответа
# @dp.message_handler(state=Form.play_1)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    us_id = message.from_user.id
    if answer.lower() == right_answer.lower():
        await message.reply(emojis.encode(f'Верно! :eight_spoked_asterisk: \n'
                                          f'/fastrule - cоздать/изменить правило для {question} \n'
                                          ), reply_markup=correct_kb)
        await state.finish()
    else:
        await message.reply(emojis.encode('Неправильно :red_circle: \n'
                                          'Попробуйте ещё раз \n'
                                          ), reply_markup=un_correct_ans_kb)


# @dp.callback_query_handler(text='hint_btn', state=Form.play_1)
async def hint_call(callback: types.CallbackQuery, state: FSMContext):
    us_id = callback.message.from_user.id
    user_rule_from_base = await show_my_rule(us_id, question_id)
    if user_rule_from_base:
        if chosen_theme != 'флаг-страна':
            await callback.message.reply(
                f'Ваше мнемоническое правило для {question} "{user_rule_from_base}", попробуйте отгадать ещё раз\n'
                f'/hint_max - ответ', reply_markup=un_correct_max_kb)
        else:
            await bot.send_photo(callback.message.chat.id, photo=question,
                                 caption="Ваше мнемоническое правило, попробуйте отгадать ещё раз\n /hint_max - "
                                         "ответ ", reply_markup=un_correct_max_kb)
    else:
        if chosen_theme != 'флаг-страна':
            await callback.message.reply(
                f'У вас нет мнемонического правила для "{question}", поробуйте отгадать ещё раз \n'
                , reply_markup=un_correct_max_kb)
        else:
            await bot.send_photo(callback.message.chat.id, photo=question,
                                 caption="У вас нет мнемонического правила для этого вопроса"
                                         " поробуйте отгадать ещё раз",
                                 reply_markup=un_correct_max_kb)
    await callback.answer()


# @dp.callback_query_handler(text='hint_max_btn', state=Form.play_1)
async def answer_check(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.reply(emojis.encode(f'Ответ: {right_answer} \n'
                                               ), reply_markup=correct_kb)
    await callback.answer()


def register_handlers_exam_train(dp: Dispatcher):
    dp.register_callback_query_handler(process_exam_menu, state = '*', text='exam_btn')
    dp.register_callback_query_handler(new_train, state='*', text='newtrain1')
    dp.register_callback_query_handler(tutorial_guide, state='*', text='go1')
    dp.register_message_handler(asking, state=Form.play_1)
    dp.register_callback_query_handler(hint_call, state=Form.play_1, text='hint_btn')
    dp.register_callback_query_handler(answer_check, state='*', text='hint_max_btn')