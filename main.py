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


class Income(Base):

    __tablename__ = 'income'

    id = Column(Integer, primary_key=True)
    index_sal = Column(Integer, primary_key=False, default=0)
    sum_sal = Column(Integer, primary_key=False, default=0)
    name_sal = Column(String(100), default='Не указано описание')
    user_id = Column(Integer)
    date = Column(default=datetime.now)

    def __repr__(self):
        return '<Income %r>' % self.id


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

kb2 = ReplyKeyboardMarkup(resize_keyboard=True,
                          one_time_keyboard=True
                         ) #аргументы
kb3 = ReplyKeyboardMarkup(resize_keyboard=True,
                          one_time_keyboard=True
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
b10 = KeyboardButton('Статистика по времени')
b11 = KeyboardButton('Подробная статистика')
b12 = KeyboardButton('Назад')
b13 = KeyboardButton('Главное меню')



kb.add(b8).insert(b9)
kb1.add(b3).add(b4).insert(b5).add(b6).insert(b7).add(b1)
kb2.add(b11).add(b13)
kb3.add(b13)


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



    # создаем подключение к нашей БД
    engine = create_engine('postgresql://main:123@localhost:5432/purchases', echo=True)

    # создаем сессию (открытие сессии)
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(Registration).filter(Registration.email == login).first()

    if user == None:
        await message.answer('Такой пользователь в системе не зарегистрирован! '
                             'Попробуйте снова /start или зарегистрируйтесь на site.ru')

    else:
        db_password = user.psw
        if check_password_hash(db_password, password):
            await bot.send_message(chat_id=message.from_id,
                                   text='Вы успешно вошли в свой аккаунт',
                                   parse_mode='HTML',
                                   reply_markup=kb1
                                   )
            await RegisteredUser.user_registered.set()

        else:
            await message.answer('Пароль подвел! '
                                 'Попробуйте снова /start')

    session.close()
    engine.dispose()  # NOTE: close required before dispose


async def get_incomes(message: types.Message, login):

    # создаем подключение к нашей БД
    engine = create_engine('postgresql://main:123@localhost:5432/purchases', echo=True)

    # создаем сессию (открытие сессии)
    Session = sessionmaker(bind=engine)
    session = Session()

    user_id = session.query(Registration).filter(Registration.email == login).first()

    income = session.query(Income).filter(Income.user_id == user_id.id).order_by(Income.date.desc()).all()

    sum_income = 0
    sum_incomes_for_today = 0
    sum_incomes_for_week = 0
    sum_incomes_for_month = 0
    to_day = datetime.today().date()

    for e in income:

        print(e.sum_sal)

        sum_income += e.sum_sal
        for_date = e.date.date()
        # разница в днях между сегодня и датой из бд
        a = to_day - for_date
        a = a.days
        if a < 1:
            sum_incomes_for_today += e.sum_sal
        elif a < 7:
            sum_incomes_for_week += e.sum_sal
        elif a < 30:
            sum_incomes_for_month += e.sum_sal

    sum_incomes_for_week += sum_incomes_for_today
    sum_incomes_for_month += sum_incomes_for_week

    await bot.send_message(chat_id=message.from_id,
                           text=f'Доход за cегодня= {sum_incomes_for_week} \n'
                                f'Доход за неделю = {sum_incomes_for_week} \n'
                                f'Доход за неделю = {sum_incomes_for_week} \n'
                                f'Доход за неделю = {sum_incomes_for_week} \n',

                           parse_mode='HTML'
                           )


    session.close()
    engine.dispose()  # NOTE: close required before dispose

async def get_more_in_incomes(message: types.Message, login):

    # создаем подключение к нашей БД
    engine = create_engine('postgresql://main:123@localhost:5432/purchases', echo=True)

    # создаем сессию (открытие сессии)
    Session = sessionmaker(bind=engine)
    session = Session()

    user_id = session.query(Registration).filter(Registration.email == login).first()

    income = session.query(Income).filter(Income.user_id == user_id.id).order_by(Income.date.desc()).all()

    for e in income:
        await bot.send_message(chat_id=message.from_id,
                               text=f'Категория / Индекс: {e.index_sal} \n'
                                    f'Цена: {e.sum_sal} \n'
                                    f'Название: {e.name_sal} \n'
                                    f'Дата: {e.date.date()} \n',

                               parse_mode='HTML'
                               )


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

@dp.message_handler(commands=['start'], state='*')
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


@dp.message_handler(content_types='text', state=RegisteredUser.user_registered)
async def user_incomes(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Главное меню':
            await bot.send_message(chat_id=message.from_id,
                                   text = "типо меню",
                                   parse_mode='HTML',
                                   reply_markup=kb1)

        if message.text == 'Статистика доходов':
            await bot.send_message(chat_id=message.from_id,
                                   text = "тут доходы",
                                   parse_mode='HTML',
                                   reply_markup=kb2)
            await get_incomes(message, data['login'])

        if message.text == 'Подробная статистика':
            await bot.send_message(chat_id=message.from_id,
                                   text = "тут  по больше",
                                   parse_mode='HTML',
                                   reply_markup=kb3)
            await get_more_in_incomes(message, data['login'])


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
    await state.reset_state(with_data=False)
    await check_profile(message, data['login'], data['password'])


# Обработка клавиатуры, которая появляется после регистрации
# @dp.message_handler(content_types=['text'], state=RegisteredUser.user_registered)
# async def user_incomes(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if message.text == 'Статистика доходов':
#             await bot.send_message(chat_id=message.from_id,
#                                    text = "тут доходы",
#                                    parse_mode='HTML',
#                                    reply_markup=kb2)
#             await get_incomes(message, data['login'])
#             await RegisteredUser.more_about_incomes.set()


# @dp.message_handler(content_types=['text'], state=RegisteredUser.more_about_incomes)
# async def user_incomes(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if message.text == 'Подробная статистика':
#             print(data)
#             await bot.send_message(chat_id=message.from_id,
#                                    text = "тут  по больше",
#                                    parse_mode='HTML',
#                                    reply_markup=kb3)
#             await get_more_in_incomes(message, data['login'])
#             await state.set_state(RegisteredUser.user_registered)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



