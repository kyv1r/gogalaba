import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

API_TOKEN = '7447722752:AAEi4c46wy7Z9Rqlsr7Qf78Q6V1wav6u-es'

# Загрузка обученной модели
model = load_model('modelimg.h5')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, отправь мне фото и я проверю есть там санта или нет.")


# Обработчик изображений
@dp.message_handler(content_types=ContentType.PHOTO)
async def classify_image(message: types.Message):
    photo = message.photo[-1]
    photo_file = await bot.download_file_by_id(photo.file_id)

    # Преобразование изображения
    image = Image.open(io.BytesIO(photo_file.read())).resize((150, 150))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    # Классификация изображения
    prediction = model.predict(image)[0][0]
    result = "Санта Клаус" if prediction > 0.5 else "Не санта клаус"

    await message.reply(f"На этом изображении: {result}")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
