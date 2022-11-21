from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import emojis

menu_btn = InlineKeyboardButton('Меню', callback_data='mmenu')
technic_btn = InlineKeyboardButton(emojis.encode('Техники :school_satchel:'), callback_data='technic1')
subject_btn = InlineKeyboardButton(emojis.encode('Выбрать тему для запоминания'), callback_data='subject1')
exam_btn = InlineKeyboardButton(emojis.encode('Заниматься :mortar_board:'), callback_data='exam_btn')
example_btn = InlineKeyboardButton('Примеры', callback_data='examples')
example_1_btn = InlineKeyboardButton('Пример, метод ЦБК', callback_data='example_1')
example_2_btn = InlineKeyboardButton('Пример, метод синонимов', callback_data='example_2')
example_3_btn = InlineKeyboardButton('Пример, метод ассоциаций', callback_data='example_3')
cancel_btn = InlineKeyboardButton(emojis.encode('Выход :x:'), callback_data='cancel1')
newtrain_btn = InlineKeyboardButton('Тренировка', callback_data='newtrain_1')
go_btn = InlineKeyboardButton(emojis.encode('Начать :white_check_mark:'), callback_data='go1')
fast_rule_btn = InlineKeyboardButton('Создать мнемо-правило', callback_data='fast_rule1')
hint_btn = InlineKeyboardButton('Посмотреть мнемо-правило', callback_data='hint_btn')
hint_max_btn = InlineKeyboardButton('Ответ', callback_data='hint_max_btn')
continue_btn = InlineKeyboardButton('Продолжить', callback_data='go1')
rules_btn = InlineKeyboardButton(emojis.encode('Мнемо-правила :scroll:'), callback_data='rules_btn')
rules_show_btn = InlineKeyboardButton('Посмотреть созданные правила', callback_data='rules_show_btn')
rules_create_btn = InlineKeyboardButton('Создать мнемо-правило', callback_data='rules_create_btn')
rules_create_show_quest_btn = InlineKeyboardButton('Создать мнемо-правило', callback_data='rules_create_show_quest_btn')
rules_show_questions = InlineKeyboardButton('Ещё примеры', callback_data='rules_create_show_next_btn')
rules_show_next_rules_btn = InlineKeyboardButton('Ещё правила', callback_data='rules_show_next_rules_btn')

inline_kb = InlineKeyboardMarkup(row_width=1).add(technic_btn, example_btn, subject_btn, newtrain_btn, rules_btn)  # Главное Меню
inline_kb2 = InlineKeyboardMarkup(row_width=1).add(technic_btn, newtrain_btn, rules_btn)  # Меню после выбора темы
cancel_kb = InlineKeyboardMarkup(row_width=1).add(cancel_btn)  # Возврат в меню
technic_kb = InlineKeyboardMarkup(row_width=1).add(cancel_btn)  # Мнемотехники
exam_kb = InlineKeyboardMarkup(row_width=1).add(newtrain_btn, rules_btn, cancel_btn)  # Меню начала тренироки
go_kb = InlineKeyboardMarkup(row_width=1).add(go_btn)  # начать тренировку
correct_kb = InlineKeyboardMarkup(row_width=1).add(go_btn, fast_rule_btn, cancel_btn)
un_correct_ans_kb = InlineKeyboardMarkup(row_width=1).add(hint_btn, cancel_btn)
un_correct_max_kb = InlineKeyboardMarkup(row_width=1).add(hint_max_btn)
continue_kb = InlineKeyboardMarkup(row_width=1).add(continue_btn, cancel_btn)
rule_kb = InlineKeyboardMarkup(row_width=1).add(rules_create_show_quest_btn, rules_show_btn, cancel_btn)
rule_kb_2 = InlineKeyboardMarkup(row_width=1).add(rules_create_btn, rules_show_questions,cancel_btn)
rule_kb_3 = InlineKeyboardMarkup(row_width=1).add(rules_create_btn, rules_show_next_rules_btn,cancel_btn)
example_kb = InlineKeyboardMarkup(row_width=1).add(example_1_btn, example_2_btn, example_3_btn, cancel_btn)

kb_subjects = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton(text= 'страна-столица')
b2 = KeyboardButton(text= 'даты, история РФ')
b3 = KeyboardButton(text= 'правовые аббревиатуры')
b4 = KeyboardButton(text= 'флаг-страна')
b5 = KeyboardButton(text= 'столица-страна')
b6 = KeyboardButton(text= 'литературные определения')
b7 = KeyboardButton(text= 'архитектура, понятия')
kb_subjects.add(b1,b2).add(b3,b4).add(b5, b6).add(b7)