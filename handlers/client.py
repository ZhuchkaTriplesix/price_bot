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
user_data = {}
json_data = "user_list.json"
push_data = "users_time.json"


class NotificationOrder(StatesGroup):
    choosing_notification = State()  # used
    choosing_add_notification = State()  # used
    response_notification_state = State()
    time_add_notification_state = State()  # used


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
        await state.set_state(NotificationOrder.choosing_notification)


@router.callback_query(NotificationOrder.choosing_add_notification, F.data == "Time_add_yes")
async def add_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите удобное для вас время")
    await state.set_state(NotificationOrder.time_add_notification_state)


@router.callback_query(NotificationOrder.choosing_add_notification, F.data == "Time_add_no")
async def answer_no(callback: CallbackQuery):
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


@router.callback_query(NotificationOrder.choosing_notification, F.data == "change_time")
async def edit_notification(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите время:")
    await state.set_state(NotificationOrder.response_notification_state)


@router.message(NotificationOrder.response_notification_state)
async def time_change_notification(message: Message):
    user_id = message.from_user.id
    user_id = f"{user_id}"
    data = json_support.read_inf(push_data)
    user_time = message.text
    c = {user_id: user_time}
    data.update(c)
    json_support.write_inf(data, push_data)
    await message.answer(f"Вы успешно поменяли время на {user_time}.")


@router.callback_query(NotificationOrder.choosing_notification, F.data == "off_notification")
async def delete_notification(callback: CallbackQuery):
    user_id = callback.message.chat.id
    user_id = f"{user_id}"
    data = json_support.read_inf(push_data)
    del data[user_id]
    json_support.write_inf(data, push_data)
    await callback.message.answer("Уведомление было отключено")


@router.message(F.text == '/clear')
async def clear(message: Message):
    data = json_support.read_inf(json_data)
    user_id = message.from_user.id
    user_id = f"{user_id}"
    del data[user_id]
    json_support.write_inf(data, json_data)
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
    user_id = callback.message.chat.id
    user_id = f"{user_id}"
    case = case_translation(callback.data)
    await callback.message.answer(f"Вы добавили {case}.")
    data = json_support.read_inf(json_data)
    cases_list =[]
    if user_id in data.keys():
        cases_list = data[user_id]
    else:
        pass
    if callback.data not in cases_list or user_id not in data.keys():
        cases_list.append(callback.data)
        c = {user_id: cases_list}
        data.update(c)
        json_support.write_inf(data, json_data)
        print(f"{user_id},{callback.message.chat.first_name} add {case}")
    else:
        pass


@router.message(F.text == "/help")
async def help_func(message: Message):
    await message.answer(
        "Commands:\n/start\n/cases - check your case list prices\n/add_case - add cases to your list\n/update - update your list in database")


@router.message()
async def echo(message: Message):
    await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")
