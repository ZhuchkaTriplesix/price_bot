from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


owners_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/give_vip")], [KeyboardButton(text="/add_admin")], [KeyboardButton(text="/delete_admin")], [KeyboardButton(text="/admin_list")], [KeyboardButton(text="/del_item")], [KeyboardButton(text="/kill")]],
    resize_keyboard=True,
    one_time_keyboard=False,
)


