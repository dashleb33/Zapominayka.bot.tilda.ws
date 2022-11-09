from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Keyboards import *
from work_with_base import *


async def on_startup(_):
    await db_start()


bot = Bot(token="5752954362:AAE0_BaG6xe8Vc_4OFIYLsTZpUzQjgiB0DI")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
lst = []

# variables
question = ''
question_create = ''
question_id = ''
chosen_theme = 'страна-столица'
dict_ques_answ = []
right_answer = ''
must_find = ''
flag = ''
all_themes = ''


#  Машина состояний
class Form(StatesGroup):
    teaching = State()
    ask_eche_primer = State()
    strana = State()
    pravilo = State()
    play = State()
    prodolzhaem = State()
    chose_theme = State()
    chose_theme_btn = State()
    play_1 = State()
    mem_rule = State()
    mem_rule_crt = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global us_id
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    await save_user_in_base(us_id,us_name, us_sname, username)
    await message.reply(emojis.encode("Привет :wave:\n Выберите, пожалуйста, меню: \n"),
                                        reply_markup=inline_kb)


# ВЫЗОВ МЕНЮ
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    global us_id, us_name, us_sname, username
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    await message.reply(emojis.encode("Привет :wave:\n Выберите, пожалуйста, меню: \n"
                                          "/subject - выбор темы для изучения \n"
                                          "/technic - техники запоминания \n"
                                          "/exam - начать заниматься"),
                                        reply_markup=inline_kb)


# ОТМЕНА
@dp.callback_query_handler(state='*', text='cancel1')
async def cancel_call(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer("Вы вышли из режима, список доступных команд\n"
                                  "Техники - для просмотра техник \n"
                                  "Темы - для выбора темы запоминания\n"
                                  "Начать - чтобы начать заниматься",
                                  reply_markup=inline_kb)
    await callback.answer()


# ТЕМЫ
@dp.callback_query_handler(text='subject1')
async def show_subjects(callback: types.CallbackQuery):
    global all_themes
    all_themes = await select_all_themes_from_base()
    await callback.message.answer(emojis.encode('Выберите и напишите тему для занятий из предложенных: :arrow_down:'))
    await callback.message.answer('\n'.join(all_themes))
    await Form.chose_theme_btn.set()
    await callback.answer()


# ВЫБОР ТЕМЫ
@dp.message_handler(state=Form.chose_theme_btn)
async def chose_theme(message: types.Message, state: FSMContext):
    global chosen_theme
    answer = message.text.lower()
    if answer in all_themes:
        chosen_theme = answer
        await message.reply(emojis.encode(f'Тема установлена "{chosen_theme}"\n'
                                          f'Теперь вы можете начать заниматься или изучить техники мнемоники'),
                            reply_markup=inline_kb)
        await state.finish()
    else:
        await message.reply(
            emojis.encode('Данной темы нет в списке, попробуйте ещё раз. \nДля выхода нажмите'),
            reply_markup=cancel_kb)


# ТЕХНИКИ ЗАПОМИНАНИЯ
@dp.callback_query_handler(text='technic1')
async def technic_call(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f"В нашем боте используются следующие техники запоминания:"
                                                "1. _Название_: :slot_machine: *Метод ЦБК* \n"
                                                "_Краткое описание_: Техника основана на условном соответствии между "
                                                "согласными буквами и цифрами "
                                                " от :zero:  до :nine: . "
                                                " Дату необходимо перевести в слова, а из слов составить фразу "
                                                "связанную с запоминаемой датой \n "
                                                "\n"
                                                "2._Название_:  :loop: *Метод синонимов* \n"
                                                "_Краткое описание_: Техника основана на построении связной "
                                                "цепочки:chains: "
                                                "между словом которое необходимо запомнить со словами схожими по "
                                                "значению и лексическому толкованию с запоминаемым словом. \n "
                                                "\n"
                                                "3._Название_:  :wavy_dash:  *Метод Ассоциаций* \n"
                                                "_Краткое описание_: Метод основан на построении связи между двумя "
                                                "или более явлениями - "
                                                "Так, например, когда вы видите идущего с лыжами человека — вы "
                                                "вспоминаете о зиме (иными словами, "
                                                " лыжи:snowboarder:  ассоциируются с зимой:cold_face:\n ")
                                  , parse_mode='MARKDOWN', reply_markup=technic_kb)
    await callback.answer()


@dp.callback_query_handler(text='technic_1')
async def technic_1_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'_Пример_:  1-ГЖ. 2-ДТ. 3-КХ. 4-ЧЩ. 5-ПБ. 6-ШЛ. 7-СЗ. 8-ВФ. 9-РЦ. '
                                                f'0-НМ.\n1608 - год '
                                                f'изобретения телескопа:telescope: . 1608 = 16 и 08. *Г*аи*ш*ник '
                                                f'неводом вытащил телескоп. '
                                                f'Г-1,Ш-6. Н-0, В-8. Гаишник:oncoming_police_car:  и '
                                                f'невод:fishing_pole_and_fish: '
                                                f' -ключевые слова, первые две согласных которых зашифрованы в цифры.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()


@dp.callback_query_handler(text='technic_2')
async def technic_2_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'Пример: Если Вам необходимо запомнить сложное словосочетание '
                                                f'(международная конвенция),'
                                                f' достаточно просто запомнить слова, близкие по значению к '
                                                f'запоминаемым: '
                                                f'международный :earth_asia: - мировой, конвенция :scroll: - условие.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()


@dp.callback_query_handler(text='technic_3')
async def technic_3_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'_Пример_: Необходимо запомнить два слова *КОТ* :cat:  и *МОЛОКО* '
                                                f':baby_bottle: . '
                                                f'Связь при ассоциации должна быть необычной, нестандартной, '
                                                f'невероятной. '
                                                f'\n *КОТ* плавает:swimmer:  в стакане с *МОЛОКОМ*.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()


@dp.callback_query_handler(text='exam_btn')
async def process_exam_menu(callback: types.CallbackQuery):
    await callback.message.answer("Доступны следующие команды: \n"
                                  "Тренировка - для проверки знаний \n"
                                  "Правила - посмотреть своим мнемонические правила",
                                  reply_markup=exam_kb)
    await callback.answer()


# ПРИСТУПИТЬ К ТРЕНИРОВКЕ
@dp.callback_query_handler(text='newtrain1')
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
@dp.callback_query_handler(text='go1')
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
@dp.message_handler(state=Form.play_1)
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


@dp.callback_query_handler(text='hint_btn', state=Form.play_1)
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


@dp.callback_query_handler(text='hint_max_btn', state=Form.play_1)
async def answer_check(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.reply(emojis.encode(f'Ответ: {right_answer} \n'
                                               ), reply_markup=correct_kb)
    await callback.answer()


@dp.callback_query_handler(state ='*', text='fast_rule1')
async def fast_create_rule(callback: types.CallbackQuery):
    global question, question_create, question_create_answer
    global flag

    question_id, question_create, question_create_answer, *other = await select_everything_for_rule(question)
    us_id = callback.message.from_user.id
    user_rule_from_base = await show_my_rule(us_id, question_id)
    if user_rule_from_base:
        await callback.message.answer(f'Ваше текущее мнемоническое правило {user_rule_from_base}',
                                      f'Cейчас создадим новое, если вы не хотите, нажмите /cancel',
                                      reply_markup=cancel_kb)
        flag = 'update_pravilo'
        await Form.mem_rule_crt.set()
        await callback.message.answer(f'Введите правило\n'
                                      f'Тема: {chosen_theme} \n'
                                      f'Вопрос: {question_create}\n'
                                      f'Ответ: {question_create_answer} \n')
    else:
        await callback.message.answer(f'Введите правило\n'
                                      f'Тема: {chosen_theme} \n'
                                      f'Вопрос: {question_create}\n'
                                      f'Ответ: {question_create_answer} \n')
        await Form.mem_rule_crt.set()
        flag = 'create_pravilo'
    await callback.answer()


# раздел "правила"
@dp.callback_query_handler(text='rules_btn')
async def rules_btn_menu(callback: types.CallbackQuery):
    await callback.message.answer(f'Тема, на которую вы будете смотреть/создавать правила это "{chosen_theme}" '
                                  f'для выбора другой нажмите "Темы"', reply_markup=rule_kb)
    await callback.answer()

# Показать правила
@dp.callback_query_handler(text='rules_show_btn')
async def rules_show(callback: types.CallbackQuery):
        global all_rules
        all_rules = await show_all_my_rules(chosen_theme)
        await callback.message.answer(f'Будут показаны мнемонические правила по теме: {chosen_theme}')
        if all_rules:
            all_rules_5_f = all_rules[0:5]
            if chosen_theme not in ['флаг-страна']:
                for_print2 = [(f"Вопрос: {question}, Ответ: {answer}, Правило: {rule}") for question, answer, rule in all_rules_5_f]
                await callback.message.answer('\n'.join(for_print2), reply_markup=rule_kb_3, parse_mode='MARKDOWN')
            else:
                for i in all_rules_5_f:
                    question, answer, rule, *other = i
                    await bot.send_photo(chat_id=callback.message.chat.id, photo=question)
                    await callback.message.answer(f'Ответ: {answer}, Правило: {rule}')
                await callback.message.answer('Показать еще правила?', reply_markup=rule_kb_3, parse_mode='MARKDOWN')
            all_rules = all_rules[5:]
        else:
           await callback.message.answer(f'У вас нет правил')


@dp.callback_query_handler(text='rules_show_next_rules_btn')
async def rules_show_next_rules(callback: types.CallbackQuery):
    global all_rules
    if all_rules:
        all_rules_5_f = all_rules[0:5]
        for_print2 = [(f"Вопрос: {question}, Ответ: {answer}, Правило: {rule}") for answer, question, rule in
                      all_rules_5_f]
        await callback.message.answer('\n'.join(for_print2), reply_markup=rule_kb_3, parse_mode='MARKDOWN')
        all_rules = all_rules[5:]
    else:
        await callback.message.answer('Правил больше нет', reply_markup=rule_kb_3)




@dp.callback_query_handler(text='rules_show_questions')
async def rules_create_show_next(callback: types.CallbackQuery):
    global dict_ques_answ
    prom = dict_ques_answ[0:5]
    for_print = [(f"Вопрос: {question}, Ответ: {answer}") for number, question, answer in prom]
    await callback.message.answer('\n'.join(for_print), reply_markup=rule_kb_2, parse_mode='MARKDOWN')
    dict_ques_answ = dict_ques_answ[5:]


@dp.callback_query_handler(text='rules_create_show_quest_btn')
async def process_registration(callback: types.CallbackQuery):
    global question
    global question_id
    global chosen_theme
    global dict_ques_answ
    await callback.message.answer(f'Сейчас вы создадите свое мнемоническое правило \n бот будет показывать по 5 '
                                  'вопросов и ответов, \n Для создания правила на '
                                  f'"создать правило" \n Тема: {chosen_theme} ', reply_markup=rule_kb_2)
    if chosen_theme:
        flag = True  # тема выбрана - печатаем с текстом "сгенерированы вопросы по теме"
    else:
        chosen_theme = ('страна-столица')
        flag = False
    dict_ques_answ = await select_questions_for_theme(chosen_theme)
    await callback.answer()

@dp.callback_query_handler(text='rules_create_show_next_btn')
async def rules_create_show_next(callback: types.CallbackQuery):
    global dict_ques_answ
    prom = dict_ques_answ[0:5]
    if chosen_theme not in ['флаг-страна']:
        for_print = [(f"Вопрос: {question}, Ответ: {answer}") for number, question, answer in prom]
        await callback.message.answer('\n'.join(for_print), reply_markup=rule_kb_2, parse_mode='MARKDOWN')
        dict_ques_answ = dict_ques_answ[5:]
    else:
        for i in prom:
            number, question, answer = i
            await bot.send_photo(chat_id=callback.message.chat.id, photo=question)
            await callback.message.answer(f'Ответ: {answer}')

@dp.callback_query_handler(text='rules_create_btn')
async def create_button_1(callback: types.CallbackQuery):
    await callback.message.answer('Сейчас вы создадите мнемоническое правило')
    await Form.mem_rule.set()
    await callback.message.answer('Введите вопрос, для ответа на который хотите создать правило, регистр неважен')
    await callback.answer()


# раздел "правила", проверка, что правила нет
@dp.message_handler(state=Form.mem_rule)
async def rule_ask(message: types.Message, state: FSMContext):
    global question_create
    global question_id
    global question_create_answer
    global flag
    global must_find
    global us_id
    quest_to_create_rule = message.text
    is_there_this_question = await is_there_question_in_base(quest_to_create_rule, chosen_theme)
    if is_there_this_question:
        question_id, question_create, question_create_answer, *other = await select_everything_for_rule(quest_to_create_rule)
        us_id = message.from_user.id
        user_rule_from_base = await show_my_rule(us_id, question_id)
        if user_rule_from_base:
            await message.answer(f'Ваше текущее мнемоническое правило {user_rule_from_base}'
                                          f'Cейчас создадим новое, если вы не хотите, нажмите /cancel',
                                          reply_markup=cancel_kb)
            # возможно стоит прописать внутренний cancel для отмены конкретного действия
            flag = 'update_pravilo'
            await Form.mem_rule_crt.set()
            await message.answer('Теперь введите правило')
        else:
            await message.answer(f'Тема: {chosen_theme}\n'
                                 f'Вопрос: {question_create} \n Ответ: {question_create_answer}')
            await Form.mem_rule_crt.set()
            await message.answer('Введите правило')
            flag = 'create_pravilo'
    else:
        await message.reply(emojis.encode('Данного вопроса нет в списке, попробуйте ещё раз. \nДля выхода нажмите'),
                            reply_markup=cancel_kb)



# раздел "правила", создание правила
@dp.message_handler(state=Form.mem_rule_crt)
async def ust_pravilo(message: types.Message, state: FSMContext):
    global must_find
    global flag
    pravilo = message.text

    if flag == 'update_pravilo':
        await update_my_rule(pravilo, us_id, question_id)
        await message.reply(f'Правило для {question_create} успешно обновлено "{pravilo}"')
        await state.finish()
        await message.reply(f'.',
                            reply_markup=continue_kb)
    elif flag == 'create_pravilo':
        await create_my_rule(us_id, question_id, pravilo)
        await message.reply(f'Правило для {question_create} успешно создано "{pravilo}"')
        await state.finish()
        await message.reply(f'.', reply_markup=continue_kb)


# Отмена действия пользователя
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Вы вышли из режима, список доступных команд\n"
                        "/subject - выбор темы для изучения \n"
                        "/technic - техники запоминания \n"
                        "/exam - начать заниматься")


# хэндлер для остальных сообщений
@dp.message_handler()
async def process_registration(message: types.Message):
    await message.reply('Пожалуйста, выберите команду из меню, для вызова команд наберите /help')


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
