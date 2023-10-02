import steammarket as sm
import telebot
import token

with open("token.txt", "r") as TOKEN:
    bot_token = TOKEN.readline()

bot = telebot.TeleBot(bot_token)



