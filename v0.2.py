from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import sqlite3
import random as r
import emojis

bot = Bot(token="5548506324:AAGlp5yCab-_8zG2X6RgtOjYzDM9Bjh6rbs")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
conn = sqlite3.connect('all_in_one_base.db', check_same_thread=False)
cursor = conn.cursor()
lst = []

# variables
question = ''
question_create = ''
question_id = ''
chosen_theme = ''
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


# добавление пользователя в базу данных
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO user_id_base (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


def db_create_rule(user_id, mnemonic_rule):
    cursor.execute('INSERT INTO user_rules (user_if_plus_question, mnemonic_rule) VALUES (?, ?)',
                   (user_id, mnemonic_rule))
    conn.commit()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    try:
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
    except:
        print('пользователь в базе')
    finally:
        await message.reply(emojis.encode("Привет :wave:\n Выберите, пожалуйста, меню: \n"
                                          "/subject - выбор темы для изучения \n"
                                          "/technic - техники запоминания \n"
                                          "/exam - начать заниматься"))


# место инлайн клавиатуры
menu_btn = InlineKeyboardButton('Меню', callback_data='mmenu')
technic_btn = InlineKeyboardButton('Техники', callback_data='technic1')
subject_btn = InlineKeyboardButton('Темы', callback_data='subject1')
exam_btn = InlineKeyboardButton('Начать', callback_data='exam_btn')
technic_1_btn = InlineKeyboardButton('Техника 1', callback_data='technic_1')
technic_2_btn = InlineKeyboardButton('Техника 2', callback_data='technic_2')
technic_3_btn = InlineKeyboardButton('Техника 3', callback_data='technic_3')
cancel_btn = InlineKeyboardButton('Выход', callback_data='cancel1')
newtrain_btn = InlineKeyboardButton('Тренировка', callback_data='newtrain1')
# configure_btn = InlineKeyboardButton('Посмотреть созданные', callback_data='configure1')
# show_empty_btn = InlineKeyboardButton('Показать пустые', callback_data='show_empty1')
create_btn = InlineKeyboardButton('Создать правило', callback_data='create_btn')
go_btn = InlineKeyboardButton('Начать', callback_data='go1')
fast_rule_btn = InlineKeyboardButton('Создать правило', callback_data='fast_rule1')
hint_btn = InlineKeyboardButton('Посмотреть правило', callback_data='hint_btn')
hint_max_btn = InlineKeyboardButton('Ответ', callback_data='hint_max_btn')
continue_btn = InlineKeyboardButton('Продолжить', callback_data='go1')

inline_kb = InlineKeyboardMarkup(row_width=1).add(technic_btn,
                                                  subject_btn, exam_btn)  # Главное Меню
inline_kb2 = InlineKeyboardMarkup(row_width=1).add(technic_btn)  # Меню после выбора темы
cancel_kb = InlineKeyboardMarkup(row_width=1).add(cancel_btn)  # Возврат в меню
technic_kb = InlineKeyboardMarkup(row_width=1).add(technic_1_btn, technic_2_btn,
                                                   technic_3_btn, cancel_btn)  # Мнемотехники
exam_kb = InlineKeyboardMarkup(row_width=1).add(newtrain_btn, create_btn, cancel_btn)  # Меню начала тренироки
go_kb = InlineKeyboardMarkup(row_width=1).add(go_btn)  # начать тренировку
correct_kb = InlineKeyboardMarkup(row_width=1).add(go_btn, fast_rule_btn, cancel_btn)
un_correct_ans_kb = InlineKeyboardMarkup(row_width=1).add(hint_btn, cancel_btn)
un_correct_max_kb = InlineKeyboardMarkup(row_width=1).add(hint_max_btn)
continue_kb = InlineKeyboardMarkup(row_width=1).add(continue_btn, cancel_btn)


# ВЫЗОВ МЕНЮ
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    try:
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
    finally:
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
                                  "/subject - выбор темы для изучения \n"
                                  "/technic - техники запоминания \n"
                                  "/exam - начать заниматься",
                                  reply_markup=inline_kb)
    await callback.answer()


# ТЕМЫ
@dp.callback_query_handler(text='subject1')
async def show_subjects(callback: types.CallbackQuery):
    global all_themes
    cursor.execute('SELECT DISTINCT theme FROM questions_base')
    all_themes = [i[0] for i in cursor.fetchall()]
    await callback.message.answer(emojis.encode('Выберите и напишите тему для занятий из предложенных: :arrow_down:'))
    await callback.message.answer('\n'.join(all_themes))
    await Form.chose_theme_btn.set()
    await callback.answer()


# ВЫБОР ТЕМЫ
@dp.message_handler(state=Form.chose_theme_btn)
async def chose_theme(message: types.Message, state: FSMContext):
    global chosen_theme
    answer = message.text
    if answer in all_themes:
        chosen_theme = answer
        await message.reply(emojis.encode(f'Тема установлена "{chosen_theme}"\n'
                                          f'Теперь вы можете начать заниматься или изучить техники мнемоники \n'
                                          f'/technic - техники запоминания :school_satchel: \n'
                                          f'/exam - начать заниматься :mortar_board:'),
                            reply_markup=inline_kb2)
        await state.finish()
    else:
        await message.reply(
            emojis.encode('Данной темы нет в списке, попробуйте ещё раз. \nДля выхода нажмите /cancel :x: '),
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
                                                "/exam1 - для примера \n"
                                                "\n"
                                                "2._Название_:  :loop: *Метод синонимов* \n"
                                                "_Краткое описание_: Техника основана на построении связной "
                                                "цепочки:chains: "
                                                "между словом которое необходимо запомнить со словами схожими по "
                                                "значению и лексическому толкованию с запоминаемым словом. \n "
                                                "/exam2 - для примера\n\n"
                                                "3._Название_:  :wavy_dash:  *Метод Ассоциаций* \n"
                                                "_Краткое описание_: Метод основан на построении связи между двумя "
                                                "или более явлениями - "
                                                "Так, например, когда вы видите идущего с лыжами человека — вы "
                                                "вспоминаете о зиме (иными словами, "
                                                " лыжи:snowboarder:  ассоциируются с зимой:cold_face:\n "
                                                "/exam3 - для примера"
                                                "\n\n Для выхода нажмите /cancel :x:")
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
                                  "/newtrain - проверка знаний \n"
                                  "/create - создать мнемоническое правило",
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
        cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE theme = '{chosen_theme}'")
        dict_ques_answ = cursor.fetchall()
        r.shuffle(dict_ques_answ)
        await callback.message.answer(emojis.encode(f'Сгененированы вопросы по теме "{chosen_theme}"\n'
                                                    f'/go для продолжения :white_check_mark:'),
                                      reply_markup=go_kb)
    else:
        chosen_theme = 'страна-столица'
        cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE theme = 'страна-столица'")
        dict_ques_answ = cursor.fetchall()
        r.shuffle(dict_ques_answ)
        await callback.message.answer(emojis.encode(f'Тема не выбрана, сгененированы вопросы '
                                                    f'по теме "страна-столица" \n'
                                                    f'/go для продолжения :white_check_mark:'),
                                      reply_markup=go_kb)
    await callback.answer()


# НАЧАТЬ
@dp.callback_query_handler(text='go1')
async def tutorial_guide(callback: types.CallbackQuery):
    global right_answer
    global question
    global question_id
    play_tuple = dict_ques_answ.pop()
    question_id = play_tuple[0]
    question = play_tuple[1]
    right_answer = play_tuple[2]
    if chosen_theme != 'флаг-страна':
        await callback.message.answer(emojis.encode(f' "{question}"  \n \n'
                                                    '/cancel :x: - для выхода'),
                                      reply_markup=cancel_kb)
    else:
        print(question)
        await bot.send_photo(chat_id=callback.message.chat.id, photo=question)
        await callback.message.answer(reply_markup=cancel_kb)
    await Form.play_1.set()
    await callback.answer()


# раздел "игра", проверка ответа
@dp.message_handler(state=Form.play_1)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    us_id = message.from_user.id
    if answer.lower() == right_answer.lower():
        await message.reply(emojis.encode(f'Верно! :eight_spoked_asterisk: \n'
                                          f' /go для продолжения :white_check_mark: \n \n '
                                          f'/fastrule - cоздать/изменить правило для {question} \n'
                                          f' /cancel :x: - для выхода'))
        await state.finish()
    # elif answer == '/hint':
    #     must_find = str(us_id) + '_' + str(question_id)
    #     try:
    #         cursor.execute(f"SELECT mnemonic_rule FROM user_rules WHERE user_id_plus_question = '{must_find}'")
    #         data = cursor.fetchone()
    #         data = str(*data)
    #         if chosen_theme != 'флаг-страна':
    #             await message.reply(f'Ваше мнемоническое правило для {question} "{data}", попробуйте отгадать ещё раз\n'
    #                                 f'/hint_max - ответ')
    #         else:
    #             await bot.send_photo(message.chat.id, photo=question,
    #                                  caption="Ваше мнемоническое правило, попробуйте отгадать ещё раз\n /hint_max - "
    #                                          "ответ ")
    #
    #     except:
    #         if chosen_theme != 'флаг-страна':
    #             await message.reply(f'У вас нет мнемонического правила для "{question}", поробуйте отгадать ещё раз \n'
    #                                 f' /hint_max - ответ')
    #         else:
    #             await bot.send_photo(message.chat.id, photo=question,
    #                                  caption="У вас нет мнемонического правила для этого вопроса"
    #                                          " поробуйте отгадать ещё раз \n /hint_max - ответ")
    # elif answer == '/hint_max':
    #     await state.finish()
    #     await message.reply(emojis.encode(f'Ответ: {right_answer} \n'
    #                                       f'/fastrule - cоздать/изменить правило для {question} \n'
    #                                       f'/go - для продолжения :white_check_mark: \n \n '
    #                                       f' /cancel :x: - для выхода'))
    else:
        await message.reply(emojis.encode('Неправильно :red_circle: \n'
                                          'Попробуйте ещё раз \n'
                                          '/hint  - для подсказки \n \n'
                                          '/cancel :x: - для выхода'), reply_markup=un_correct_ans_kb)


@dp.callback_query_handler(text='hint_btn', state=Form.play_1)
async def hint_call(callback: types.CallbackQuery, state: FSMContext):
    us_id = callback.message.from_user.id
    must_find = str(us_id) + '_' + str(question_id)
    try:
        cursor.execute(f"SELECT mnemonic_rule FROM user_rules WHERE user_id_plus_question = '{must_find}'")
        data = cursor.fetchone()
        data = str(*data)
        if chosen_theme != 'флаг-страна':
            await callback.message.reply(
                f'Ваше мнемоническое правило для {question} "{data}", попробуйте отгадать ещё раз\n'
                f'/hint_max - ответ', reply_markup=un_correct_max_kb)
        else:
            await bot.send_photo(callback.message.chat.id, photo=question,
                                 caption="Ваше мнемоническое правило, попробуйте отгадать ещё раз\n /hint_max - "
                                         "ответ ", reply_markup=un_correct_max_kb)
    except:
        if chosen_theme != 'флаг-страна':
            await callback.message.reply(
                f'У вас нет мнемонического правила для "{question}", поробуйте отгадать ещё раз \n'
                f' /hint_max - ответ', reply_markup=un_correct_max_kb)
        else:
            await bot.send_photo(callback.message.chat.id, photo=question,
                                 caption="У вас нет мнемонического правила для этого вопроса"
                                         " поробуйте отгадать ещё раз \n /hint_max - ответ",
                                 reply_markup=un_correct_max_kb)
    await callback.answer()


@dp.callback_query_handler(text='hint_max_btn', state=Form.play_1)
async def answer_check(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.reply(emojis.encode(f'Ответ: {right_answer} \n'
                                               f'/fastrule - cоздать/изменить правило для {question} \n'
                                               f'/go - для продолжения :white_check_mark: \n \n '
                                               f' /cancel :x: - для выхода'), reply_markup=correct_kb)
    await callback.answer()


@dp.callback_query_handler(text='fast_rule1')
async def fast_create_rule(callback: types.CallbackQuery):
    global question
    global question_create
    global question_create_answer
    global flag
    global must_find
    cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE question = '{question}'")
    data = cursor.fetchall()
    question_id = data[0][0]
    question_create = data[0][1]
    question_create_answer = data[0][2]
    us_id = callback.message.from_user.id
    must_find = str(us_id) + '_' + str(question_id)
    try:
        cursor.execute(f"SELECT mnemonic_rule FROM users_rules WHERE mnemonic_rule = '{must_find}'")
        data1 = cursor.fetchall()
        await callback.message.answer(f'Ваше текущее мнемоническое правило {data1}',
                                      f'Cейчас создадим новое, если вы не хотите, нажмите /cancel',
                                      reply_markup=cancel_kb)
        flag = 'update_pravilo'
        await Form.mem_rule_crt.set()
        await callback.message.answer(f'Введите правило\n'
                                      f'Тема: {chosen_theme} \n'
                                      f'Вопрос: {question_create}\n'
                                      f'Ответ: {question_create_answer} \n')
    except:
        await callback.message.answer(f'Введите правило\n'
                                      f'Тема: {chosen_theme} \n'
                                      f'Вопрос: {question_create}\n'
                                      f'Ответ: {question_create_answer} \n')
        await Form.mem_rule_crt.set()
        flag = 'create_pravilo'
    await callback.answer()


# раздел "правила", создать новое правило
@dp.callback_query_handler(text='create_btn')
async def process_registration(callback: types.CallbackQuery):
    await callback.message.answer('Сейчас вы создадите свое мнемоническое правило')
    await Form.mem_rule.set()
    await callback.message.answer('Введите вопрос, для ответа на который хотите создать правило, регистр неважен')
    await callback.answer()


# раздел "правила", проверка, что правила нет
@dp.callback_query_handler(state=Form.mem_rule)
async def chose_strana(callback: types.CallbackQuery, state: FSMContext):
    global question_create
    global question_create_answer
    global flag
    global must_find
    quest_to_create_rule = callback.message.text
    # try:
    await callback.message.answer(quest_to_create_rule)
    cursor.execute(
        f"SELECT question_id, question, right_answer FROM questions_base WHERE question = '{quest_to_create_rule}'")
    # except:
    #    await message.reply('Такого вопроса нет\n Для выхода из режима выберите /cancel ')
    data = cursor.fetchall()
    await callback.message.answer(data)
    question_id = data[0][0]
    question_create = data[0][1]
    question_create_answer = data[0][2]
    us_id = callback.message.from_user.id
    must_find = str(us_id) + '_' + str(question_id)
    try:
        cursor.execute(f"SELECT mnemonic_rule FROM users_rules WHERE mnemonic_rule = '{must_find}'")
        data1 = cursor.fetchall()
        await callback.message.answer(f'Ваше текущее мнемоническое правило {data1}'
                                      f'Cейчас создадим новое, если вы не хотите, нажмите /cancel',
                                      reply_markup=cancel_kb)
        # возможно стоит прописать внутренний cancel для отмены конкретноего действия
        flag = 'update_pravilo'
        await Form.mem_rule_crt.set()
        await callback.message.answer('Теперь введите правило')

    except:
        await callback.message.answer(f'У вас действительно нет такого мнемонического правила, сейчас его создадим')
        await Form.mem_rule_crt.set()
        await callback.message.answer('Теперь введите правило')
        flag = 'create_pravilo'


# раздел "правила", создание правила
@dp.message_handler(state=Form.mem_rule_crt)
async def ust_pravilo(message: types.Message, state: FSMContext):
    global must_find
    global flag
    pravilo = message.text

    if flag == 'update_pravilo':
        cursor.execute('UPDATE user_rules SET mnemonic_rule == ? WHERE user_id_plus_question == ?',
                       (pravilo, must_find))
        await message.reply(f'Правило для {question_create} успешно обновлено "{pravilo}"')
        conn.commit()
        await state.finish()
        await message.reply(f'Для продолжения игры нажмите /go, для выхода /cancel',
                            reply_markup=continue_kb)
    elif flag == 'create_pravilo':
        cursor.execute('INSERT INTO user_rules (user_id_plus_question, mnemonic_rule) VALUES (?, ?)',
                       (must_find, pravilo))
        await message.reply(f'Правило для {question_create} успешно создано "{pravilo}"')
        conn.commit()
        await state.finish()
        await message.reply(f'Для продолжения игры нажмите /go, для выхода /cancel',
                            reply_markup=continue_kb)


# Отмена действия пользователя
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Вы вышли из режима, список доступных команд\n"
                        "/subject - выбор темы для изучения \n"
                        "/technic - техники запоминания \n"
                        "/exam - начать заниматься")


@dp.message_handler(commands=['subject'])
async def show_subjects(message: types.Message):
    global all_themes
    cursor.execute('SELECT DISTINCT theme FROM questions_base')
    print(all_themes)
    all_themes = [i[0] for i in cursor.fetchall()]
    await message.reply(emojis.encode('Выберите и напишите тему для занятий из предложенных: :arrow_down:'))
    await message.reply('\n'.join(all_themes))
    await Form.chose_theme.set()


@dp.message_handler(state=Form.chose_theme)
async def chose_theme(message: types.Message, state: FSMContext):
    global chosen_theme
    answer = message.text
    if answer in all_themes:
        chosen_theme = answer
        await message.reply(emojis.encode(f'Тема установлена "{chosen_theme}"\n'
                                          f'Теперь вы можете начать заниматься или изучить техники мнемоники \n'
                                          f'/technic - техники запоминания :school_satchel: \n'
                                          f'/exam - начать заниматься :mortar_board:'))
        await state.finish()
    else:
        await message.reply(
            emojis.encode('Данной темы нет в списке, попробуйте ещё раз. \nДля выхода нажмите /cancel :x: '))


@dp.message_handler(commands=['technic'])
async def show_subjects(message: types.Message):
    await message.reply(emojis.encode(f'В нашем боте используются следующие техники запоминания:'
                                      '1. _Название_: :slot_machine: *Метод ЦБК* \n'
                                      '_Краткое описание_: Техника основана на условном соответствии между согласными буквами и цифрами'
                                      ' от :zero:  до :nine: . '
                                      ' Дату необходимо перевести в слова, а из слов составить фразу связанную с запоминаемой датой \n'
                                      '/exam1 - для примера \n'
                                      '\n'
                                      '2._Название_:  :loop: *Метод синонимов* \n'
                                      '_Краткое описание_: Техника основана на построении связной цепочки:chains:  '
                                      'между словом которое необходимо запомнить со словами схожими по значению и лексическому толкованию с запоминаемым словом. \n'
                                      '/exam2 - для примера\n\n'
                                      '3._Название_:  :wavy_dash: *Метод Ассоциаций* \n'
                                      '_Краткое описание_: Метод основан на построении связи между двумя или более явлениями - '
                                      'Так, например, когда вы видите идущего с лыжами человека — вы вспоминаете о зиме (иными словами,'
                                      ' лыжи:snowboarder:  ассоциируются с зимой:cold_face:\n '
                                      '/exam3 - для примера'
                                      '\n\n Для выхода нажмите /cancel :x:')
                        , parse_mode='MARKDOWN')


# примеры к правилам

@dp.message_handler(commands=['exam1'])
async def example_1(message: types.Message):
    await message.reply(
        emojis.encode(f'_Пример_:  1-ГЖ. 2-ДТ. 3-КХ. 4-ЧЩ. 5-ПБ. 6-ШЛ. 7-СЗ. 8-ВФ. 9-РЦ. 0-НМ.\n1608 - год '
                      f'изобретения телескопа:telescope: . 1608 = 16 и 08. *Г*аи*ш*ник неводом вытащил телескоп.'
                      f'Г-1,Ш-6. Н-0, В-8. Гаишник:oncoming_police_car:  и невод:fishing_pole_and_fish: '
                      f' -ключевые слова, первые две согласных которых зашифрованы в цифры.'), parse_mode='MARKDOWN')


@dp.message_handler(commands=['exam2'])
async def example_2(message: types.Message):
    await message.reply(emojis.encode(f'Пример: Если Вам необходимо запомнить сложное словосочетание '
                                      f'(международная конвенция),'
                                      f' достаточно просто запомнить слова, близкие по значению к запоминаемым: '
                                      f'международный :earth_asia: - мировой, конвенция :scroll: - условие.'),
                        parse_mode='MARKDOWN')


@dp.message_handler(commands=['exam3'])
async def example_3(message: types.Message):
    await message.reply(
        emojis.encode(f'_Пример_: Необходимо запомнить два слова *КОТ* :cat:  и *МОЛОКО* :baby_bottle: . '
                      f'Связь при ассоциации должна быть необычной, нестандартной, невероятной.'
                      f'\n *КОТ* плавает:swimmer:  в стакане с *МОЛОКОМ*.'), parse_mode='MARKDOWN')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(emojis.encode("Выберите, пожалуйста, меню: \n"
                                      "/subject - выбор темы для изучения \n"
                                      "/technic - техники запоминания \n"
                                      "/exam - начать заниматься"))


# Раздел train
@dp.message_handler(commands=['train'])
async def tutorial_guide(message: types.Message):
    await message.reply("Давайте приступим к обучению. \n "
                        "Сейчас мы покажем вам примеры мнемонических правил"
                        " для столиц стран, которые помогут вам обучиться, поставьте +, если готовы")
    global lst
    lst = list(range(1, 11))
    r.shuffle(lst)
    await Form.teaching.set()


# Продолжение раздела train
@dp.message_handler(state=Form.teaching)
async def show_examples(message: types.Message, state: FSMContext):
    if lst:
        a = lst.pop()
        cursor.execute(f'SELECT * FROM capitals WHERE  ID = {a}')
        data = cursor.fetchone()
        await message.reply(f'Страна: {data[1]} \n Cтолица: {data[2]} \n Мнемоническое правило: {data[3]}')
        if lst:
            await message.reply(f'Показать ещё пример? \n Для выхода нажмите /cancel')
            await Form.ask_eche_primer.set()
        else:
            await message.reply(f'Этот пример был последним, перейдите, пожалуйста, в другой раздел /help')


# Продолжение раздела train, ещё пример показать?
@dp.message_handler(state=Form.ask_eche_primer)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    if answer in ['yes', 'y', 'да', '+']:
        await Form.teaching.set()
    else:
        await message.reply('Выберете другое в меню.')
        await state.finish()


@dp.message_handler(commands=['exam'])
async def process_exam_menu(message: types.Message):
    await message.reply("Доступны следующие команды: \n"
                        "/newtrain - проверка знаний \n"
                        # "/configure - посмотреть созданные мнемонические правила \n"
                        # "/show_empty - показать пустые карточки по выбранной теме\n"
                        "/create - создать мнемоническое правило")


# Раздел "игра", генерация последовательности
@dp.message_handler(commands=['newtrain'])
async def new_train(message: types.Message):
    global question
    global question_id
    global chosen_theme
    global dict_ques_answ
    if chosen_theme:
        cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE theme = '{chosen_theme}'")
        dict_ques_answ = cursor.fetchall()
        r.shuffle(dict_ques_answ)
        await message.reply(emojis.encode(f'Сгененированы вопросы по теме "{chosen_theme}"\n'
                                          f'/go для продолжения :white_check_mark:'))
    else:
        chosen_theme = 'страна-столица'
        cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE theme = 'страна-столица'")
        dict_ques_answ = cursor.fetchall()
        r.shuffle(dict_ques_answ)
        await message.reply(emojis.encode(f'Тема не выбрана, сгененированы вопросы '
                                          f'по теме "страна-столица" \n'
                                          f'/go для продолжения :white_check_mark:'))


# раздел "новая игра", начало игры
@dp.message_handler(commands=['go'])
async def tutorial_guide(message: types.Message):
    global right_answer
    global question
    global question_id
    play_tuple = dict_ques_answ.pop()
    print(play_tuple)
    question_id = play_tuple[0]
    question = play_tuple[1]
    right_answer = play_tuple[2]
    if chosen_theme != 'флаг-страна':
        await message.reply(emojis.encode(f' "{question}"  \n \n'
                                          '/cancel :x: - для выхода'))
    else:
        print(question)
        await bot.send_photo(chat_id=message.chat.id, photo=question)
    await Form.play.set()


# раздел "игра", проверка ответа
@dp.message_handler(state=Form.play)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    us_id = message.from_user.id
    if answer.lower() == right_answer.lower():
        await message.reply(emojis.encode(f'Верно! :eight_spoked_asterisk: \n'
                                          f' /go для продолжения :white_check_mark: \n \n '
                                          f'/fastrule - cоздать/изменить правило для {question} \n'
                                          f' /cancel :x: - для выхода'))
        await state.finish()
    elif answer == '/hint':
        must_find = str(us_id) + '_' + str(question_id)
        try:
            cursor.execute(f"SELECT mnemonic_rule FROM user_rules WHERE user_id_plus_question = '{must_find}'")
            data = cursor.fetchone()
            data = str(*data)
            if chosen_theme != 'флаг-страна':
                await message.reply(f'Ваше мнемоническое правило для {question} "{data}", попробуйте отгадать ещё раз\n'
                                    f'/hint_max - ответ')
            else:
                await bot.send_photo(message.chat.id, photo=question,
                                     caption="Ваше мнемоническое правило, попробуйте отгадать ещё раз\n /hint_max - ответ ")

        except:
            if chosen_theme != 'флаг-страна':
                await message.reply(f'У вас нет мнемонического правила для "{question}", поробуйте отгадать ещё раз \n'
                                    f' /hint_max - ответ')
            else:
                await bot.send_photo(message.chat.id, photo=question,
                                     caption="У вас нет мнемонического правила для этого вопроса"
                                             " поробуйте отгадать ещё раз \n /hint_max - ответ")
    elif answer == '/hint_max':
        await state.finish()
        await message.reply(emojis.encode(f'Ответ: {right_answer} \n'
                                          f'/fastrule - cоздать/изменить правило для {question} \n'
                                          f'/go - для продолжения :white_check_mark: \n \n '
                                          f' /cancel :x: - для выхода'))
    else:
        await message.reply(emojis.encode('Неправильно :red_circle: \n'
                                          'Попробуйте ещё раз \n'
                                          '/hint  - для подсказки \n \n'
                                          '/cancel :x: - для выхода'))


@dp.message_handler(commands=['fastrule'])
async def fast_create_rule(message: types.Message):
    global question
    global question_create
    global question_create_answer
    global flag
    global must_find
    cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE question = '{question}'")
    data = cursor.fetchall()
    question_id = data[0][0]
    question_create = data[0][1]
    question_create_answer = data[0][2]
    us_id = message.from_user.id
    must_find = str(us_id) + '_' + str(question_id)
    try:
        cursor.execute(f"SELECT mnemonic_rule FROM users_rules WHERE mnemonic_rule = '{must_find}'")
        data1 = cursor.fetchall()
        await message.reply(f'Ваше текущее мнемоническое правило {data1}'
                            f'Cейчас создадим новое, если вы не хотите, нажмите /cancel')
        flag = 'update_pravilo'
        await Form.pravilo.set()
        await message.reply(f'Введите правило\n'
                            f'Тема: {chosen_theme} \n'
                            f'Вопрос: {question_create}\n'
                            f'Ответ: {question_create_answer} \n')
    except:
        await message.reply(f'Введите правило\n'
                            f'Тема: {chosen_theme} \n'
                            f'Вопрос: {question_create}\n'
                            f'Ответ: {question_create_answer} \n')
        await Form.pravilo.set()
        flag = 'create_pravilo'


# раздел "правила", показать мнемонические правила
@dp.message_handler(commands=['configure'])
async def process_registration(message: types.Message):
    await message.reply('Покажем все мнемонические правила, которые у вас есть')
    cursor.execute(f'SELECT Country, Capital, mnemonic_rule FROM capitals WHERE  mnemonic_rule IS NOT NULL')
    data = cursor.fetchall()
    await message.reply(f'{data}')


# раздел "пустые правила", показать страны для которых нет правил
@dp.message_handler(commands=['show_empty'])
async def process_registration(message: types.Message):
    await message.reply('Сейчас мы покажем все страны и их столицы, для которых у вас нет мнемонических правил')
    cursor.execute("SELECT Country, Capital  FROM capitals WHERE mnemonic_rule IS NULL")
    data = cursor.fetchall()
    await message.reply(data)
    await message.reply('Если хотите создать правило, выберите /create')


# раздел "правила", создать новое правило
@dp.message_handler(commands=['create'])
async def process_registration(message: types.Message):
    await message.reply('Сейчас вы создадите свое мнемоническое правило')
    await Form.strana.set()
    await message.reply('Введите вопрос, для ответа на который хотите создать правило, регистр неважен')


# раздел "правила", проверка, что правила нет
@dp.message_handler(state=Form.strana)
async def chose_strana(message: types.Message, state: FSMContext):
    global question_create
    global question_create_answer
    global flag
    global must_find
    quest_to_create_rule = message.text
    # try:
    await message.reply(quest_to_create_rule)
    cursor.execute(
        f"SELECT question_id, question, right_answer FROM questions_base WHERE question = '{quest_to_create_rule}'")
    # except:
    #    await message.reply('Такого вопроса нет\n Для выхода из режима выберите /cancel ')
    data = cursor.fetchall()
    await message.reply(data)
    question_id = data[0][0]
    question_create = data[0][1]
    question_create_answer = data[0][2]
    us_id = message.from_user.id
    must_find = str(us_id) + '_' + str(question_id)
    try:
        cursor.execute(f"SELECT mnemonic_rule FROM users_rules WHERE mnemonic_rule = '{must_find}'")
        data1 = cursor.fetchall()
        await message.reply(f'Ваше текущее мнемоническое правило {data1}'
                            f'Cейчас создадим новое, если вы не хотите, нажмите /cancel')
        flag = 'update_pravilo'
        await Form.pravilo.set()
        await message.reply('Теперь введите правило')

    except:
        await message.reply(f'У вас действительно нет такого мнемонического правила, сейчас его создадим')
        await Form.pravilo.set()
        await message.reply('Теперь введите правило')
        flag = 'create_pravilo'


# раздел "правила", создание правила
@dp.message_handler(state=Form.pravilo)
async def ust_pravilo(message: types.Message, state: FSMContext):
    global must_find
    global flag
    pravilo = message.text

    if flag == 'update_pravilo':
        cursor.execute('UPDATE user_rules SET mnemonic_rule == ? WHERE user_id_plus_question == ?',
                       (pravilo, must_find))
        await message.reply(f'Правило для {question_create} успешно обновлено "{pravilo}"')
        conn.commit()
        await state.finish()
        await message.reply(f'Для продолжения игры нажмите /go, для выхода /cancel')
    elif flag == 'create_pravilo':
        cursor.execute('INSERT INTO user_rules (user_id_plus_question, mnemonic_rule) VALUES (?, ?)',
                       (must_find, pravilo))
        await message.reply(f'Правило для {question_create} успешно создано "{pravilo}"')
        conn.commit()
        await state.finish()
        await message.reply(f'Для продолжения игры нажмите /go, для выхода /cancel')


# хэндлер для остальных сообщений
@dp.message_handler()
async def process_registration(message: types.Message):
    await message.reply('Пожалуйста, выберите команду из меню, для вызова команд наберите /help')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
