from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import select
import string

storage = MemoryStorage()
Base = declarative_base()


class Registration(Base):
    __tablename__ = 'registration'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    psw = Column(String(500), nullable=True)


    def __repr__(self):
        return '<Registration %r>' % self.id


bot = Bot('6646799075:AAEnWRsy-xNajNzdMYpwAx7PJoupa52V2f8')
dp = Dispatcher(bot, storage=MemoryStorage())


class ProfileStatesGroup(StatesGroup):
    user_name = State()
    user_password = State()


class RegisteredUser(StatesGroup):
    user_registered = State()



kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True
                         ) #аргументы

kb1 = ReplyKeyboardMarkup(resize_keyboard=True,
                          ) #аргументы

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/start')
b3 = KeyboardButton('Добавление чека')
b4 = KeyboardButton('Добавление доходов')
b5 = KeyboardButton('Добавление расхоов')
b6 = KeyboardButton('Статистика доходов')
b7 = KeyboardButton('Статистика расходов')
b8 = KeyboardButton('Вход в сервис')
b9 = KeyboardButton('Регистрация')



kb.add(b8).insert(b9)
kb1.add(b3).add(b4).insert(b5).add(b6).insert(b7).add(b1)


async def get_user_data(message: types.Message):
    # создаем подключение к нашей БД
    engine = create_engine('postgresql://main:123@localhost:5432/purchases', echo=True)

    # создаем сессию (открытие сессии)
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(Registration).all()

    for user in users:
        await message.answer(f'{user.id},{user.email}')

    session.close()
    engine.dispose()  # NOTE: close required before dispose!


async def check_profile(message: types.Message, login, password):
    print(login, password)
    # создаем подключение к нашей БД
    engine = create_engine('postgresql://main:123@localhost:5432/purchases', echo=True)

    # создаем сессию (открытие сессии)
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(Registration).all()

    for user in users:
        if user.email != login:
            await message.answer('Такой пользователь в системе не зарегистрирован!')
            break
        else:
            db_password = user.psw
            if check_password_hash(db_password, password):
                await bot.send_message(chat_id=message.from_id,
                                       text='Вы успешно вошли в свой аккаунт',
                                       parse_mode='HTML',
                                       reply_markup=kb1
                                       )

                break
            else:
                await message.answer('Пароль подвел!')
                break

    session.close()
    engine.dispose()  # NOTE: close required before dispose





HELP_COMMAND = """
<b>/help</b> - <em>Список команд</em>
<b>/start</b> - <em>Старт бота</em>
<b>/photo</b> - <em>Фото</em>
"""



@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_id,
                           text = HELP_COMMAND,
                           parse_mode='HTML')


@dp.message_handler(commands=['data'])
async def some_data(message: types.Message):
    await get_user_data(message)


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_id,
                           text = "Добро пожаловать, для начала взаимодествия войдите в аккаунт или зарегистрируйтесьб на сайте site.ru",
                           parse_mode='HTML',
                           reply_markup=kb)


@dp.message_handler()
async def log_in_command(message: types.Message):
    if message.text == 'Вход в сервис':
        await bot.send_message(chat_id=message.from_id,
                               text = "Введите логин:",
                               parse_mode='HTML')
        await ProfileStatesGroup.user_name.set()


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.user_name)
async def load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await message.reply("Теперь пароль:")
    await ProfileStatesGroup.next()


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.user_password)
async def load_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    await message.reply("Принял данные!")
    await check_profile(message, data['login'], data['password'])
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



