from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="5271510735:AAHXRoH2Y6znSMu4bna3SCPws8sji32VZAE")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

