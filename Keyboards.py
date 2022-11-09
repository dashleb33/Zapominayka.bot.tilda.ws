from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import emojis

menu_btn = InlineKeyboardButton('Меню', callback_data='mmenu')
technic_btn = InlineKeyboardButton(emojis.encode('Техники :school_satchel:'), callback_data='technic1')
subject_btn = InlineKeyboardButton(emojis.encode('Темы :scroll:'), callback_data='subject1')
exam_btn = InlineKeyboardButton(emojis.encode('Заниматься :mortar_board:'), callback_data='exam_btn')
technic_1_btn = InlineKeyboardButton('Пример, метод ЦБК', callback_data='technic_1')
technic_2_btn = InlineKeyboardButton('Пример, метод синонимов', callback_data='technic_2')
technic_3_btn = InlineKeyboardButton('Пример, метод ассоциаций', callback_data='technic_3')
cancel_btn = InlineKeyboardButton(emojis.encode('Выход :x:'), callback_data='cancel1')
newtrain_btn = InlineKeyboardButton('Тренировка', callback_data='newtrain1')
go_btn = InlineKeyboardButton(emojis.encode('Начать :white_check_mark:'), callback_data='go1')
fast_rule_btn = InlineKeyboardButton('Создать правило', callback_data='fast_rule1')
hint_btn = InlineKeyboardButton('Посмотреть правило', callback_data='hint_btn')
hint_max_btn = InlineKeyboardButton('Ответ', callback_data='hint_max_btn')
continue_btn = InlineKeyboardButton('Продолжить', callback_data='go1')
rules_btn = InlineKeyboardButton(emojis.encode('Правила :scroll:'), callback_data='rules_btn')
rules_show_btn = InlineKeyboardButton('Посмотреть созданные правила', callback_data='rules_show_btn')
rules_create_btn = InlineKeyboardButton('Создать правило', callback_data='rules_create_btn')
rules_create_show_quest_btn = InlineKeyboardButton('Создать правило', callback_data='rules_create_show_quest_btn')
rules_show_questions = InlineKeyboardButton('Ещё примеры', callback_data='rules_create_show_next_btn')
rules_show_next_rules_btn = InlineKeyboardButton('Ещё правила', callback_data='rules_show_next_rules_btn')


inline_kb = InlineKeyboardMarkup(row_width=1).add(technic_btn,
                                                  subject_btn, exam_btn)  # Главное Меню
inline_kb2 = InlineKeyboardMarkup(row_width=1).add(technic_btn, newtrain_btn, rules_btn)  # Меню после выбора темы
cancel_kb = InlineKeyboardMarkup(row_width=1).add(cancel_btn)  # Возврат в меню
technic_kb = InlineKeyboardMarkup(row_width=1).add(technic_1_btn, technic_2_btn,
                                                   technic_3_btn, cancel_btn)  # Мнемотехники
exam_kb = InlineKeyboardMarkup(row_width=1).add(newtrain_btn, rules_btn, cancel_btn)  # Меню начала тренироки
go_kb = InlineKeyboardMarkup(row_width=1).add(go_btn)  # начать тренировку
correct_kb = InlineKeyboardMarkup(row_width=1).add(go_btn, fast_rule_btn, cancel_btn)
un_correct_ans_kb = InlineKeyboardMarkup(row_width=1).add(hint_btn, cancel_btn)
un_correct_max_kb = InlineKeyboardMarkup(row_width=1).add(hint_max_btn)
continue_kb = InlineKeyboardMarkup(row_width=1).add(continue_btn, cancel_btn)
rule_kb = InlineKeyboardMarkup(row_width=1).add(rules_create_show_quest_btn, rules_show_btn,subject_btn, cancel_btn)
rule_kb_2 = InlineKeyboardMarkup(row_width=1).add(rules_create_btn, rules_show_questions,cancel_btn)
rule_kb_3 = InlineKeyboardMarkup(row_width=1).add(rules_create_btn, rules_show_next_rules_btn,cancel_btn)