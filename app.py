from aiogram import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *
from markups import *

import replicate
import os


# tg_bot_token = "5911163528:AAEveMEcq_TVmkVY9UArlf39d87zZ7rr5cI"
os.environ["REPLICATE_API_TOKEN"] = "3ec86c85a469f27f9cecac6136a6ab37819ebd82"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def check_sub_channels(channels, user_id):
  for channel in channels:
    chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
    # print(chat_member['status'])
    if chat_member['status'] == 'left':
       return False
  return True



@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.chat.type == 'private':
      if await check_sub_channels(CHANNELS, message.from_user.id):
        await message.answer(f"Hello, {'<b>'}{message.from_user.full_name}{'</b>'} bu bot sun'iy intellekt yordamida neyron tarmoqdan foydalanib, inson yordamisiz suratlar chizadi",parse_mode = 'HTML')
        await message.answer(f"Natijalarni olish uchun rasmda nimani ifodalamoqchi bo'lganingizni ⚠️🇬🇧{'<b>'}INGILIZ TILIDA{'</b>'}🇬🇧⚠️ yozing",parse_mode = 'HTML')
      else:
        await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)


@dp.message_handler()
async def get_weather(message: types.Message):
  if message.chat.type == 'private':
    if await check_sub_channels(CHANNELS, message.from_user.id):
      print(message.text)
      model = replicate.models.get("stability-ai/stable-diffusion")
      version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
      for image2 in version.predict(prompt=message.text):
        print(image2)
      await bot.send_photo(message.chat.id, photo=image2, caption="Created by: @Tm_ai_bot")
    else:
      await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)

@dp.callback_query_handler(text="subchanneldone")
async def  subchanneldone(message: types.Message):
  await bot.delete_message(message.from_user.id, message.message.message_id)
  if await check_sub_channels(CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id,text=f"Salom, {'<b>'}{message.from_user.full_name}{'</b>'} bu bot sun'iy intellekt yordamida neyron tarmoqdan foydalanib, inson yordamisiz suratlar chizadi", parse_mode='HTML')
        await bot.send_message(message.from_user.id,text=f"Natijalarni olish uchun rasmda nimani ifodalamoqchi bo'lganingizni ⚠️🇬🇧{'<b>'}INGILIZ TILIDA{'</b>'}🇬🇧⚠️ yozing", parse_mode='HTML')
  else:
     await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)


if __name__ == '__main__':
    executor.start_polling(dp)