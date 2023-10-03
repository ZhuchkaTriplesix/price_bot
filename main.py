import steammarket as sm
import telebot
import json_support

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

cases_list = ["CS20 Case", "Danger Zone Case", "Clutch Case"]
user_data = {}
json_data = "user_list.json"


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("/Cases", "/Add_case", "/Update", "/Clear")
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard)


@bot.message_handler(commands=["Clear"])
def clear_list(message):
    cases_list.clear()
    bot.send_message(message.chat.id, text='You have successful cleared your list')


@bot.message_handler(commands=["cases", "Cases"])
def cases(message):
    x = ''
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys():
        for case in data[user_id]:
            case_price = sm.get_item(730, case, currency='RUB')
            x = f"{x + case}: {str(case_price['lowest_price'])} \n"
        bot.send_message(message.chat.id, f"Your cases price:\n{x}")
    else:
        bot.send_message(message.chat.id, "Ypu don't have cases in your list")


@bot.message_handler(commands=["Add_case"])
def item_list(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for btns in case_list:
        markup.add(telebot.types.InlineKeyboardButton(text=btns, callback_data=btns))
    bot.send_message(message.chat.id, text="What case do u want to add?", reply_markup=markup)


@bot.message_handler(commands=["Update"])
def update(message):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys():
        data[user_id].update(cases_list)
        json_support.write_inf(data, json_data)
        bot.send_message(message.chat.id, "Your list has been updated")
    else:
        c = {}
        c[user_id] = cases_list
        data.update(c)
        json_support.write_inf(data, json_data)
        bot.send_message(message.chat.id, "You have added your item list")
        print(message.chat.first_name, "add a new dict in json")


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data not in cases_list:
        cases_list.append(call.data)
    else:
        pass
    print(cases_list)


bot.polling(none_stop=True)
