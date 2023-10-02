import steammarket as sm
import telebot
from telebot import types

with open("token.txt", "r") as TOKEN:
    bot_token = TOKEN.readline()

bot = telebot.TeleBot(bot_token)
case_list = ["CS:GO Weapon Case 3", "Shadow Case", "Operation Wildfire Case", "Falchion Case", "Horizon Case",
             "Revolver Case", "Prisma Case", "Operation Vanguard Weapon Case", "Prisma 2 Case", "CS20 Case",
             "Danger Zone Case", "Snakebite Case", "Fracture Case", "Shattered Web Case",
             "Operation Phoenix Weapon Case", "Operation Broken Fang Case", "Chroma 2 Case", "Dreams & Nightmares Case",
             "Spectrum Case", "Chroma 3 Case", "Clutch Case", "Chroma Case", "Spectrum 2 Case", "Gamma Case",
             "eSports 2014 Summer Case", "Operation Riptide Case", "Gamma 2 Case", "Winter Offensive Weapon Case",
             "eSports 2013 Winter Case", "CS:GO Weapon Case 2", "Huntsman Weapon Case", "Glove Case",
             "Operation Breakout Weapon Case", "Operation Hydra Case", "Operation Bravo Case", "eSports 2013 Case",
             "CS:GO Weapon Case"]

cases_list = []


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("/Cases", "/Case_list")
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard)


@bot.message_handler(commands=["cases", "Cases"])
def cases(message):
    print(message.from_user.id)
    for case in cases_list:
        case_price = sm.get_item(730, case, currency='RUB')
        bot.send_message(message.chat.id, case + ": " + str(case_price["lowest_price"]))


@bot.message_handler(commands=["Case_list"])
def item_list(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for btns in case_list:
        markup.add(telebot.types.InlineKeyboardButton(text=btns, callback_data=btns))
    bot.send_message(message.chat.id, text="What case do u want to add?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data not in cases_list:
        cases_list.append(call.data)
    else:
        pass
    print(cases_list)


bot.polling(none_stop=True)
