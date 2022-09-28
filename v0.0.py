
from aiogram import Bot, Dispatcher, executor, types

# Объект бота
bot = Bot(token="5648590997:AAHYn7hqS7ZJMfpQmwC7wgq6BGAFuN8qY4E")
# Диспетчер для бота
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Обучение", "Проверка"]
    keyboard.add(*buttons)
    await message.answer("Какой режим вы бы хотели попробовать?", reply_markup=keyboard)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
