from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import string

bot = Bot('6646799075:AAEnWRsy-xNajNzdMYpwAx7PJoupa52V2f8')
dp = Dispatcher(bot)


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



