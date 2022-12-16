from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="5648590997:AAFWb068s2ba8Y8kck4xizE-hrY7dXXwUeg")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

