from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS


lang = InlineKeyboardMarkup(
  row_width=1,
  inline_keyboard=[
    [
      InlineKeyboardButton(text="Kanal", url='https://t.me/tmBots_bek'),
    ],
    [
      InlineKeyboardButton(text="Obuna bo'ldim", callback_data="subchanneldone"),
    ]
  ]
)