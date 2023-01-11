import aiogram
from aiogram import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *
from markups import *
import os
import openai
import base64






# tg_bot_token = "5911163528:AAEveMEcq_TVmkVY9UArlf39d87zZ7rr5cI"
# os.environ["REPLICATE_API_TOKEN"] = "3ec86c85a469f27f9cecac6136a6ab37819ebd82"
openai.api_key = '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'

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
      await bot.send_message(message.from_user.id, "Generating image...")
      print("Name: " + message.from_user.full_name + "\n"
            "Username: " + message.from_user.username + "\n"
            "Request: " + message.text)
      # model = replicate.models.get("stability-ai/stable-diffusion")
      # version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
      # for image2 in version.predict(prompt=message.text):
      #   print(image2)
      openai.api_key = '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'

      imgg = openai.Image.create(
        prompt=message.text,
        n=1,
        size="512x512",
        response_format="b64_json"
      )
      # print(image2)
      for i in range(0, len(imgg['data'])):
        b64 = imgg['data'][i]['b64_json']
      with open(f'image_{i}.png', 'wb') as f:
        f.write(base64.urlsafe_b64decode(b64))


      photo = aiogram.types.input_file.InputFile("image_0.png")

      await bot.send_photo(message.chat.id, photo=photo, caption="Created by: @Tm_ai_bot")
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