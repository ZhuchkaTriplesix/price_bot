from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import steammarket as sm
import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
from case_translation import case_translation

router = Router()
cases_list = []
user_data = {}
json_data = "user_list.json"
push_data = "users_time.json"


class NotificationOrder(StatesGroup):
    choosing_notification = State()
    choosing_add_notification = State()
    response_notification_state = State()
    time_add_notification_state = State()


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer("Привет", reply_markup=kb.main)


@router.message(F.text == "/notification")
async def notification(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(push_data)
    if user_id not in data.keys():
        await message.answer("Хотите ли вы включить ежедневные уведомления?", reply_markup=kb.yes_no_keyboard)
        await state.set_state(NotificationOrder.choosing_add_notification)
    else:
        await message.answer(f"Что хотите?\nВаше текущее время уведомления: {data[user_id]}",
                             reply_markup=kb.change_off_keyboard)


@router.callback_query(NotificationOrder.choosing_add_notification, F.data == "Time_add_yes")
async def add_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите удобное для вас время")
    await state.set_state(NotificationOrder.time_add_notification_state)


@router.callback_query(NotificationOrder.choosing_add_notification, F.data == "Time_add_no")
async def answer_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Ну и хрен с тобой :(")


@router.message(NotificationOrder.time_add_notification_state)
async def time_adding(message: Message):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(push_data)
    user_time = message.text
    c = {user_id: user_time}
    data.update(c)
    json_support.write_inf(data, push_data)
    await message.answer(f"Вы добавили уведомление на {user_time}.")


@router.message(F.text == '/clear')
async def clear(message: Message):
    cases_list.clear()
    await message.answer("Локальный список ваших кейсов успешно очищен.")


@router.message(F.text == '/cases')
async def cases(message: Message):
    x = ''
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys() and len(data[user_id]) > 0:
        for case in data[user_id]:
            case_price = sm.get_item(730, case, currency='RUB')
            case = case_translation(case)
            x = f"{x + case}: {str(case_price['lowest_price'])} \n"
        await message.answer(f"Цены на ваши кейсы:\n{x}")
    else:
        await message.answer("Вы не добавили кейсы.")


@router.message(F.text == "/add_case")
async def item_list(message: Message):
    await message.answer("Какой кейс вы хотите добавить?:", reply_markup=kb.cases)


@router.callback_query()
async def answer(callback: CallbackQuery):
    case = case_translation(callback.data)
    await callback.message.answer(f"Вы добавили {case}, не забудьте обновить список /update.")
    if callback.data not in cases_list:
        cases_list.append(callback.data)
    else:
        pass
    print(cases_list)


@router.message(F.text == "/update")
async def update(message):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys():
        c = {user_id: cases_list}
        data.update(c)
        json_support.write_inf(data, json_data)
        cases_list.clear()
        await message.answer("Вы успешно обновили список кейсов.")
    else:
        c = {user_id: cases_list}
        data.update(c)
        json_support.write_inf(data, json_data)
        cases_list.clear()
        await message.answer("Вы успешно добавили ваш список кейсов.")
        print(message.chat.first_name, "add a new dict in json")


@router.message(F.text == "/help")
async def help_func(message: Message):
    await message.answer(
        "Commands:\n/start\n/cases - check your case list prices\n/add_case - add cases to your list\n/update - update your list in database")


@router.message()
async def echo(message: Message):
    await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")
