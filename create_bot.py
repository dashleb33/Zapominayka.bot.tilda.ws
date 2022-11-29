from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=":")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

