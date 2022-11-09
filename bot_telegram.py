from aiogram import Bot, Dispatcher, executor, types
from Keyboards import *
from work_with_base import *
from create_bot import dp, bot

async def on_startup(_):
    await db_start()
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


from handlers import subjects, start, cancel, technic, exam_train, rules, other
cancel.register_handlers_cancel(dp)
subjects.register_handlers_subjects(dp)
start.register_handlers_start(dp)
technic.register_handlers_technic(dp)
exam_train.register_handlers_exam_train(dp)
rules.register_handlers_rules(dp)
other.register_handlers_other(dp)



if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
