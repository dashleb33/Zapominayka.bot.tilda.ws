from aiogram import executor
from work_with_base import *
from create_bot import dp

async def on_startup(_):
    await db_start()


from handlers import subjects, start, cancel, technic, exam_train, rules, other, second_menu
cancel.register_handlers_cancel(dp)
start.register_handlers_start(dp)
second_menu.register_handlers_second_menu(dp)
subjects.register_handlers_subjects(dp)
technic.register_handlers_technic(dp)
exam_train.register_handlers_exam_train(dp)
rules.register_handlers_rules(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
