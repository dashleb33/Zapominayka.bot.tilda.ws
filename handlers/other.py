from aiogram import Dispatcher, types


# хэндлер для остальных сообщений
#@dp.message_handler()
async def other_handler(message: types.Message):
    await message.reply('Пожалуйста, выберите команду из меню, для вызова команд наберите /help')

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(other_handler)
