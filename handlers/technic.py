from Keyboards import *
from aiogram import Dispatcher,  types


# @dp.callback_query_handler(text='technic1')
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


# @dp.callback_query_handler(text='technic_1')
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


# @dp.callback_query_handler(text='technic_2')
async def technic_2_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'Пример: Если Вам необходимо запомнить сложное словосочетание '
                                                f'(международная конвенция),'
                                                f' достаточно просто запомнить слова, близкие по значению к '
                                                f'запоминаемым: '
                                                f'международный :earth_asia: - мировой, конвенция :scroll: - условие.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()


# @dp.callback_query_handler(text='technic_3')
async def technic_3_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'_Пример_: Необходимо запомнить два слова *КОТ* :cat:  и *МОЛОКО* '
                                                f':baby_bottle: . '
                                                f'Связь при ассоциации должна быть необычной, нестандартной, '
                                                f'невероятной. '
                                                f'\n *КОТ* плавает:swimmer:  в стакане с *МОЛОКОМ*.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()

def register_handlers_technic(dp: Dispatcher):
    dp.register_callback_query_handler(technic_call, state = '*', text='technic1')
    dp.register_callback_query_handler(technic_1_def, state='*', text='technic_1')
    dp.register_callback_query_handler(technic_2_def, state='*', text='technic_2')
    dp.register_callback_query_handler(technic_3_def, state='*', text='technic_3')

