from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import select
import string

Base = declarative_base()


class Registration(Base):
    __tablename__ = 'registration'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    psw = Column(String(500), nullable=True)


    def __repr__(self):
        return '<Registration %r>' % self.id


bot = Bot('6646799075:AAEnWRsy-xNajNzdMYpwAx7PJoupa52V2f8')
dp = Dispatcher(bot)


async def get_user_data(message: types.Message):
    # создаем подключение к нашей БД
    engine = create_engine('postgresql://main:123@localhost:5432/purchases', echo=True)

    # создаем сессию (открытие сессии)
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(Registration).all()

    for user in users:
        await message.answer(f'{user.id},{user.email}')

    sessionession.close()
    engine.dispose()  # NOTE: close required before dispose!




HELP_COMMAND = """
<b>/help</b> - <em>Список команд</em>
<b>/start</b> - <em>Старт бота</em>
<b>/photo</b> - <em>Фото</em>
"""

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         #one_time_keyboard=True
                         ) #аргументы
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/start')
b4 = KeyboardButton('Добавление дохода')
b5 = KeyboardButton('Добавление расхода')
b6 = KeyboardButton('Статистика дохода')
b7 = KeyboardButton('Статистика расхода')

b3 = KeyboardButton('Добавление чека')

kb.add(b1).add(b2).add(b4).add(b5).add(b6).add(b7).insert(b3)


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
                           text = "Whats up",
                           parse_mode='HTML',
                           reply_markup=kb)



@dp.message_handler(commands=['photo'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_id,
                           text = "photo",
                           parse_mode='HTML')
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



