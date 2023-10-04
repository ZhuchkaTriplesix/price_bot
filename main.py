import asyncio
import json

import aiogram.types
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
import steammarket as sm
import json_support
import keyboards as kb

with open("token.txt", "r") as TOKEN:
    bot_token = TOKEN.readline()

bot = Bot(bot_token)
dp = Dispatcher()
cases_list = []
user_data = {}
json_data = "user_list.json"
push_data = "users_time.json"


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer("Привет", reply_markup=kb.main)


@dp.message(F.text == "/notification")
async def notification(message: Message):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(push_data)
    if user_id not in data.keys():
        await message.answer("Хотите ли вы включить ежедневные уведомления?", reply_markup=kb.yes_no_keyboard)
    else:
        await message.answer(f"Что хотите?\nВаше текущее время уведомления: {data[user_id]}",
                             reply_markup=kb.change_off_keyboard)


@dp.callback_query(F.data == "Time_add_yes")
async def add_user(callback: CallbackQuery):
    await callback.message.answer("Напишите удобное для вас время")
    user_id = callback.message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(push_data)
    user_time = callback.message.text
    c = {user_id: user_time}
    data.update(c)
    json_support.write_inf(data, push_data)


@dp.callback_query(F.data == "Time_add_no")
async def answer_no(callback: CallbackQuery):
    await callback.message.answer("Ну и хрен с тобой :(")


@dp.message(F.text == '/clear')
async def clear(message: Message):
    cases_list.clear()
    await message.answer("Локальный список ваших кейсов успешно очищен.")


@dp.message(F.text == '/cases')
async def cases(message: Message):
    x = ''
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys() and len(data[user_id]) > 0:
        for case in data[user_id]:
            case_price = sm.get_item(730, case, currency='RUB')
            x = f"{x + case}: {str(case_price['lowest_price'])} \n"
        await message.answer(f"Цены на ваши кейсы:\n{x}")
    else:
        await message.answer("Вы не добавили кейсы")


@dp.message(F.text == "/add_case")
async def item_list(message: Message):
    await message.answer("Какой кейс вы хотите добавить?:", reply_markup=kb.cases)


@dp.callback_query()
async def answer(callback: CallbackQuery):
    if callback.data not in cases_list:
        cases_list.append(callback.data)
    else:
        pass
    print(cases_list)


@dp.message(F.text == "/update")
async def update(message):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys():
        c = {user_id: cases_list}
        data.update(c)
        json_support.write_inf(data, json_data)
        await message.answer("Вы успешно обновили список кейсов")
    else:
        c = {user_id: cases_list}
        data.update(c)
        json_support.write_inf(data, json_data)
        await message.answer("Вы успешно добавили ваш список кейсов")
        print(message.chat.first_name, "add a new dict in json")


@dp.message(F.text == "/help")
async def help_func(message: Message):
    await message.answer(
        "Commands:\n/start\n/cases - check your case list prices\n/add_case - add cases to your list\n/update - update your list in database")


@dp.message()
async def echo(message: Message):
    await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
