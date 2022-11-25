from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="5648590997:AAELVsuYGkQ12pIpxRGWwus7Cl4rh5Fy_QQ")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

