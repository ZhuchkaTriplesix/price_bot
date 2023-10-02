import steammarket as sm
import telebot

with open("token.txt", "r") as TOKEN:
    bot_token = TOKEN.readline()

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("Cases", "Item list")
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard)









bot.polling(none_stop=True)
