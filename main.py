import steammarket as sm
import telebot

with open("token.txt", "r") as TOKEN:
    bot_token = TOKEN.readline()

bot = telebot.TeleBot(bot_token)
cases_list = []


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("Cases", "Item list")
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def cases(message):
    if message.text in ("cases", "Cases"):
        for case in cases_list:
            case = case.lower().capitalize() + " Case"
            case_price = sm.get_item(730, case, currency='RUB')
            if case_price['success'] is False:
                bot.send_message(message.chat.id, f"Can't find item {case}")
            else:
                bot.send_message(message.chat.id, case + ": " + str(case_price["lowest_price"]))


bot.polling(none_stop=True)
