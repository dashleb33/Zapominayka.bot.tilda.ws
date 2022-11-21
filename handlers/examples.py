from Keyboards import *
from aiogram import Dispatcher,  types

# @dp.callback_query_handler(text='examples')
async def example_call(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f"Здесь можно посмотреть примеры техник")
                                  , parse_mode='MARKDOWN', reply_markup=example_kb)
    await callback.answer()

# @dp.callback_query_handler(text='example_1')
async def example_1_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f' 1-ГЖ. 2-ДТ. 3-КХ. 4-ЧЩ. 5-ПБ. 6-ШЛ. 7-СЗ. 8-ВФ. 9-РЦ. '
                                                f'0-НМ.\n1608 - год '
                                                f'изобретения телескопа:telescope: . 1608 = 16 и 08. (Г)аи(ш)ник '
                                                f'неводом вытащил телескоп. '
                                                f'Г-1,Ш-6. Н-0, В-8. Гаишник:oncoming_police_car:  и '
                                                f'невод:fishing_pole_and_fish: '
                                                f' -ключевые слова, первые две согласных которых зашифрованы в цифры.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()


# @dp.callback_query_handler(text='example_2')
async def example_2_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'Если Вам необходимо запомнить сложное словосочетание '
                                                f'(международная конвенция),'
                                                f' достаточно просто запомнить слова, близкие по значению к '
                                                f'запоминаемым: '
                                                f'международный :earth_asia: - мировой, конвенция :scroll: - условие.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()


# @dp.callback_query_handler(text='example_3')
async def example_3_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'Необходимо запомнить два слова КОТ :cat:  и МОЛОКО '
                                                f':baby_bottle: . '
                                                f'Связь при ассоциации должна быть необычной, нестандартной, '
                                                f'невероятной. '
                                                f'\n *КОТ* плавает:swimmer:  в стакане с *МОЛОКОМ*.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()

def register_handlers_examples(dp: Dispatcher):
    dp.register_callback_query_handler(example_call, state = '*', text='examples')
    dp.register_callback_query_handler(example_1_def, state='*', text='example_1')
    dp.register_callback_query_handler(example_2_def, state='*', text='example_2')
    dp.register_callback_query_handler(example_3_def, state='*', text='example_3')