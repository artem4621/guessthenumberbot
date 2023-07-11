import asyncio  # Работа с асинхронностью
import random

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command, Text  # Фильтр для /start, /...
from aiogram.types import Message  # Тип сообщения

from config import config  # Config

API_TOKEN = config.token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # Менеджер бота

statistics = {
    # 1:{
    #  'win': 0,
    #   'lose': 0
    # }
}


# dp.message - обработка сообщений
# Command(commands=['start'] Фильтр для сообщений, берём только /start
@dp.message(Command(commands=['start']))  # Берём только сообщения, являющиеся командой /start
async def start_command(message: Message):  # message - сообщение, которое прошло через фильтр
    await message.answer("Привет!Попробуй угадать число от 1 до 10\n"
                         "Напиши Да,если готов")  # Отвечаем на полученное сообщение
@dp.message(Command(commands=['statistics']))
async def get_statistics(message: Message):
    current_user_stats = statistics[message.chat.id]
    await message.answer(f'Побед {current_user_stats["win"]}\nПоражений: {current_user_stats["lose"]}')

@dp.message(Text(text='Да'))
async def handle_yes(message: Message):
    await message.answer('Отгадывай')
@dp.message()
async def handle_number(message: Message):
    if message.text.isdigit():
        number = random.randint(1, 10)
        chat_id = message.chat.id
        if not message.chat.id in statistics:
            statistics[chat_id] = {
                'lose': 0,
                'win': 0
            }
        if number == int(message.text):
            await message.answer('Вы угадали!')
            statistics[chat_id]['win'] += 1
        else:
            await message.answer('Вы проиграли!')
            statistics[chat_id]['lose'] += 1
async def main():
    try:
        print('Bot Started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':  # Если мы запускаем конкретно этот файл.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
