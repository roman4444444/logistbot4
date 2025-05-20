import logging
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv('API_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.reply("Привет! Давай рассчитаем плотность груза.\nУкажи единицу измерения (см или м):")

@dp.message_handler(lambda message: user_data.get(message.from_user.id) is not None and 'unit' not in user_data[message.from_user.id])
async def get_unit(message: types.Message):
    unit = message.text.strip().lower()
    if unit not in ['см', 'м']:
        await message.reply("Только см или м. Повтори:")
        return
    user_data[message.from_user.id]['unit'] = unit
    await message.reply("Теперь введи длину:")

@dp.message_handler(lambda message: 'length' not in user_data.get(message.from_user.id, {}))
async def get_length(message: types.Message):
    try:
        length = float(message.text.replace(',', '.'))
        user_data[message.from_user.id]['length'] = length
        await message.reply("Ширина:")
    except:
        await message.reply("Нужно число. Повтори:")

@dp.message_handler(lambda message: 'width' not in user_data.get(message.from_user.id, {}))
async def get_width(message: types.Message):
    try:
        width = float(message.text.replace(',', '.'))
        user_data[message.from_user.id]['width'] = width
        await message.reply("Высота:")
    except:
        await message.reply("Нужно число. Повтори:")

@dp.message_handler(lambda message: 'height' not in user_data.get(message.from_user.id, {}))
async def get_height(message: types.Message):
    try:
        height = float(message.text.replace(',', '.'))
        user_data[message.from_user.id]['height'] = height
        await message.reply("Вес одной коробки (кг):")
    except:
        await message.reply("Нужно число. Повтори:")

@dp.message_handler(lambda message: 'weight' not in user_data.get(message.from_user.id, {}))
async def get_weight(message: types.Message):
    try:
        weight = float(message.text.replace(',', '.'))
        user_data[message.from_user.id]['weight'] = weight
        await message.reply("Количество коробок:")
    except:
        await message.reply("Нужно число. Повтори:")

@dp.message_handler(lambda message: 'count' not in user_data.get(message.from_user.id, {}))
async def get_count(message: types.Message):
    try:
        count = int(message.text.strip())
        data = user_data[message.from_user.id]
        data['count'] = count

        l, w, h = data['length'], data['width'], data['height']
        if data['unit'] == 'см':
            l /= 100
            w /= 100
            h /= 100

        volume = l * w * h
        total_volume = volume * count
        total_weight = data['weight'] * count
        density = data['weight'] / volume

        reply = (
            f"Общий объем: {total_volume:.3f} м³\n"
            f"Общий вес: {total_weight:.2f} кг\n"
            f"Плотность: {round(density)} кг/м³"
        )
        await message.reply(reply)
        user_data.pop(message.from_user.id)

    except:
        await message.reply("Нужно целое число. Повтори:")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)