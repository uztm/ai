from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS


lang = InlineKeyboardMarkup(
  row_width=1,
  inline_keyboard=[
    [
      InlineKeyboardButton(text="Channel", url='https://t.me/tmBots_bek'),
    ],
    [
      InlineKeyboardButton(text="I SUBSCRIBED", callback_data="subchanneldone"),
    ]
  ]
)