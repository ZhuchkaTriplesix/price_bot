from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main_kb = [
    [KeyboardButton(text="/cases"),
     KeyboardButton(text="/add_case")],
    [
        KeyboardButton(text="/clear")]
]

main = ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)
cases_inline = [
    [InlineKeyboardButton(text="Оружейный кейс CS:GO", callback_data="CS:GO Weapon Case")],
    [InlineKeyboardButton(text="eSports 2013 Case", callback_data="eSports 2013 Case")],
    [InlineKeyboardButton(text="Кейс операции «Браво»", callback_data="Operation Bravo Case")],
    [InlineKeyboardButton(text="Оружейный кейс CS:GO #2", callback_data="CS:GO Weapon Case 2")],
    [InlineKeyboardButton(text="eSports 2013 Winter Case", callback_data="eSports 2013 Winter Case")],
    [InlineKeyboardButton(text="Оружейный кейс «Winter Offensive»", callback_data="Winter Offensive Weapon Case")],
    [InlineKeyboardButton(text="Оружейный кейс CS:GO #3", callback_data="CS:GO Weapon Case 3")],
    [InlineKeyboardButton(text="Оружейный кейс операции «Феникс»", callback_data="Operation Phoenix Weapon Case")],
    [InlineKeyboardButton(text="Охотничий оружейный кейс", callback_data="Huntsman Weapon Case")],
    [InlineKeyboardButton(text="Оружейный кейс операции «Прорыв»", callback_data="Operation Breakout Weapon Case")],
    [InlineKeyboardButton(text="eSports 2014 Summer Case", callback_data="eSports 2014 Summer Case")],
    [InlineKeyboardButton(text="Оружейный кейс операции «Авангард»", callback_data="Operation Vanguard Weapon Case")],
    [InlineKeyboardButton(text="Хромированный кейс", callback_data="Chroma Case")],
    [InlineKeyboardButton(text="Хромированный кейс #2", callback_data="Chroma 2 Case")],
    [InlineKeyboardButton(text="Кейс «Фальшион»", callback_data="Falchion Case")],
    [InlineKeyboardButton(text="Тёмный кейс", callback_data="Shadow Case")],
    [InlineKeyboardButton(text="Револьверный кейс", callback_data="Revolver Case")],
    [InlineKeyboardButton(text="Кейс операции «Дикое пламя»", callback_data="Operation Wildfire Case")],
    [InlineKeyboardButton(text="Хромированный кейс #3", callback_data="Chroma 3 Case")],
    [InlineKeyboardButton(text="Гамма-кейс", callback_data="Gamma Case")],
    [InlineKeyboardButton(text="Гамма-кейс #2", callback_data="Gamma 2 Case")],
    [InlineKeyboardButton(text="Перчаточный кейс", callback_data="Glove Case")],
    [InlineKeyboardButton(text="Кейс «Спектр»", callback_data="Spectrum Case")],
    [InlineKeyboardButton(text="Кейс операции «Гидра»", callback_data="Operation Hydra Case")],
    [InlineKeyboardButton(text="Кейс «Спектр 2» ", callback_data="Spectrum 2 Case")],
    [InlineKeyboardButton(text="Кейс «Решающий момент»", callback_data="Clutch Case")],
    [InlineKeyboardButton(text="Кейс «Горизонт»", callback_data="Horizon Case")],
    [InlineKeyboardButton(text="Кейс «Запретная зона»", callback_data="Danger Zone Case")],
    [InlineKeyboardButton(text="Кейс «Призма» ", callback_data="Prisma Case")],
    [InlineKeyboardButton(text="Кейс «CS20» ", callback_data="CS20 Case")],
    [InlineKeyboardButton(text="Кейс «Расколотая сеть»", callback_data="Shattered Web Case")],
    [InlineKeyboardButton(text="Кейс «Призма 2»", callback_data="Prisma 2 Case")],
    [InlineKeyboardButton(text="Кейс «Разлом»", callback_data="Fracture Case")],
    [InlineKeyboardButton(text="Кейс операции «Сломанный клык»", callback_data="Operation Broken Fang Case")],
    [InlineKeyboardButton(text="Кейс «Змеиный укус»", callback_data="Snakebite Case")],
    [InlineKeyboardButton(text="Кейс операции «Хищные воды»", callback_data="Operation Riptide Case")],
    [InlineKeyboardButton(text="Кейс «Грёзы и кошмары»", callback_data="Dreams & Nightmares Case")],
    [InlineKeyboardButton(text="Recoil Case", callback_data="Recoil Case")],
    [InlineKeyboardButton(text="Revolution Case", callback_data="Revolution Case")],
]
cases = InlineKeyboardMarkup(inline_keyboard=cases_inline)
yes_no = [
    [InlineKeyboardButton(text="Да", callback_data="Time_add_yes")],
    [InlineKeyboardButton(text="Нет", callback_data="Time_add_no")]
]
yes_no_keyboard = InlineKeyboardMarkup(inline_keyboard=yes_no, one_time_keyboiard=True)
change_off = [
    [InlineKeyboardButton(text="Поменять время", callback_data="change_time")],
    [InlineKeyboardButton(text="Выключить уведомление", callback_data="off_notification")]
]
change_off_keyboard = InlineKeyboardMarkup(inline_keyboard=change_off, one_time_keyboiard=True)

admin_keyboard = [
    [KeyboardButton(text="/add_admin"),
     KeyboardButton(text="/delete_admin")],
    [
     KeyboardButton(text="/kill"),
     KeyboardButton(text="/back")]
]
admin = ReplyKeyboardMarkup(keyboard=admin_keyboard, resize_keyboard=True)
