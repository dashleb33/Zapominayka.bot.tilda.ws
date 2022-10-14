from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import random as r

r.seed = 37

bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('Base.db', check_same_thread=False)
europe = sqlite3.connect('europe_capitals.db', check_same_thread=False)
cursor = conn.cursor()
cursor_db = europe.cursor()
lst = []


#  Машина состояний
class Form(StatesGroup):
    teaching = State()
    ask_eche_primer = State()
    strana = State()
    pravilo = State()
    play = State()
    prodolzhaem = State()


# добавление пользователя в базу данных
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ ваш бот!\n Используйте /help, чтобы узнать список всех команд")


# Меню HELP
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Доступны следующие команды:\n /register для регистрации  \n"
                        "/train для обучения\n"
                        " /newplay для игры \n"
                        "/configure - посмотреть свои мнемонические правила \n"
                        "/show_empty - показать пустые карточки \n"
                        "/create - создать свои мнемонические карточки")


# Раздел register
@dp.message_handler(commands=['register'])
async def process_registration(message: types.Message):
    await message.reply('Приступим к регистрации!\n'
                        'Это нужно, чтобы ваши мнемонические правила и прогресс сохранялись')
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
    await message.reply('Вы добавлены в базу пользователей!')


# Отмена действия пользователя
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Вы вышли из режима, список доступных команд '
                        '\n /register для регистрации  '
                        '\n /train для обучения\n'
                        " /newplay для игры \n"
                        "/configure - посмотреть свои мнемонические правила \n"
                        "/show_empty - показать пустые карточки \n"
                        "/create - создать свои мнемонические карточки")


# Раздел train
@dp.message_handler(commands=['train'])
async def tutorial_guide(message: types.Message):
        await message.reply("Давайте приступим к обучению. \n "
                            "Сейчас мы покажем вам примеры мнемонических правил"
                            " для столиц стран, которые помогут вам обучиться, поставьте +, если готовы")
        global lst
        lst = list(range(1, 11))
        r.shuffle(lst)
        await Form.teaching.set()


# Продолжение раздела train
@dp.message_handler(state=Form.teaching)
async def show_examples(message: types.Message, state: FSMContext):
    if lst:
        a = lst.pop()
        cursor_db.execute(f'SELECT * FROM capitals WHERE  ID = {a}')
        data = cursor_db.fetchone()
        await message.reply(f'Страна: {data[1]} \n Cтолица: {data[2]} \n Мнемоническое правило: {data[3]}')
        if lst:
            await message.reply(f'Показать ещё пример? \n Для выхода нажмите /cancel')
            await Form.ask_eche_primer.set()
        else:
            await message.reply(f'Этот пример был последним, перейдите, пожалуйста, в другой раздел /help')


# Продолжение раздела train, ещё пример показать?
@dp.message_handler(state=Form.ask_eche_primer)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    if answer in ['yes', 'y', 'да', '+']:
        await Form.teaching.set()
    else:
        await message.reply('Выберете другое в меню.')
        await state.finish()


# Раздел "новая игра", генерация последовательности
@dp.message_handler(commands=['newplay'])
async def tutorial_guide(message: types.Message):
    global play_primers
    play_primers = list(range(8, 13))
    r.shuffle(play_primers)
    await message.reply('Мы сгененировали уникальную последовательность для вас, нажмите /play для игры')


# раздел "новая игра", начало игры
@dp.message_handler(commands=['play'])
async def tutorial_guide(message: types.Message):
    global capital_for_play
    global strana_for_play
    id_for_play = play_primers.pop()
    cursor_db.execute(f'SELECT Country, Capital FROM capitals WHERE  ID = {id_for_play}')
    data = cursor_db.fetchone()
    strana_for_play = data[0]
    capital_for_play = data[1]
    await message.reply(f'Напишите столицу страны "{strana_for_play}"  \n'
                        'либо /cancel, чтобы выйти')
    await Form.play.set()



# раздел "игра", проверка ответа
@dp.message_handler(state=Form.play)
async def asking(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.lower() ==  capital_for_play.lower():
        await message.reply(f'Верно! для продолжения /play, для выхода /cancel ')
        await state.finish()
    elif answer == '/hint':
        cursor_db.execute('SELECT mnemonic_rule FROM capitals WHERE  Country == ?',(strana_for_play,))
        data = cursor_db.fetchone()
        data = str(*data)
        if not 'None' in data:
            await message.reply(f'Ваше мнемоническое правило для страны "{data}", попробуйте отгадать или для продолжения игры /play')
        else:
            await message.reply(f'У вас нет мнемонического правила для страны "{strana_for_play}", поробуйте отгадать ещё раз или /hint_max для ответа ')
    elif answer == '/hint_max':
        await state.finish()
        await message.reply(f'Ответ: {capital_for_play}, для продолжения игры /play, список команд /help')
    else:
        await message.reply('Неправильно, попробуйте ещё раз, для выхода /cancel, для получения подсказки /hint')


# раздел "правила", показать мнемонические правила
@dp.message_handler(commands=['configure'])
async def process_registration(message: types.Message):
    await message.reply('Покажем все мнемонические правила, которые у вас есть')
    cursor_db.execute(f'SELECT Country, Capital, mnemonic_rule FROM capitals WHERE  mnemonic_rule IS NOT NULL')
    data = cursor_db.fetchall()
    await message.reply(f'{data}')


# раздел "пустые правила", показать страны для которых нет правил
@dp.message_handler(commands=['show_empty'])
async def process_registration(message: types.Message):
    await message.reply('Сейчас мы покажем все страны и их столицы, для которых у вас нет мнемонических правил')
    cursor_db.execute("SELECT Country, Capital  FROM capitals WHERE mnemonic_rule IS NULL")
    data = cursor_db.fetchall()
    await message.reply(data)
    await message.reply('Если хотите создать правило, выберите /create')


# раздел "правила", создать новое правило
@dp.message_handler(commands=['create'])
async def process_registration(message: types.Message):
    await message.reply('Сейчас вы создадите свое мнемоническое правило')
    await Form.strana.set()
    await message.reply('Введите страну, регистр неважен')


# раздел "правила", проверка, что правила нет
@dp.message_handler(state=Form.strana)
async def chose_strana(message: types.Message, state: FSMContext):
    answer = message.text
    cursor_db.execute(f"SELECT Country, Capital  FROM capitals WHERE mnemonic_rule IS NULL")
    data = cursor_db.fetchall()
    for i in data:
        i = [j.lower() for j in i]
        if answer.lower() in i:
            global strana1
            strana1 = answer
            await Form.pravilo.set()
            await message.reply('Теперь введите правило')
            break
    else:
        await message.reply('Такой страны нет или мнемоническое правило уже установлено введите другую. \n'
                            'Для выхода из режима выберите /cancel ')


# раздел "правила", создание правила
@dp.message_handler(state=Form.pravilo)
async def ust_pravilo(message: types.Message, state: FSMContext):
    prpr = message.text
    await message.reply(prpr)
    await message.reply(strana1)
    cursor_db.execute('UPDATE capitals SET mnemonic_rule == ? WHERE Country == ?', (prpr, strana1))
    europe.commit()
    await message.reply(f'Правило для {strana1} успешно создано "{prpr}"')


# хэндлер для остальных сообщений
@dp.message_handler()
async def process_registration(message: types.Message):
    await message.reply('Пожалуйста, выберете команду из меню, для вызова команд наберите /help')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
