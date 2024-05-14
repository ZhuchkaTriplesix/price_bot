from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.fsm.context import FSMContext
from db import models
from misc import keyboards as kb
import steammarket as sm
from data.config import sell_fee

router = Router()


class AddInventory(StatesGroup):
    add_item_state = State()
    delete_item_state = State()


@router.message(F.text == "⁉️SUPPORT⁉️")
async def support(message: Message):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/support")
    if models.Users.check_vip(message.from_user.id) is True:
        await message.answer("Напишите - @ZhuchkaTriplesix")
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(F.text == "❓VIP HELP❓")
async def vip_help(message: Message):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/vip_help")
    await message.answer(
        "Команды для Vip пользователей:\n/support - Персональная помощь с ботом\n/add_item - Добавить предметы\n/my_items - Ваши предметы")


# noinspection PyTypeChecker
@router.message(F.text == "📈MY ITEMS📈")
async def my_cases(message: Message):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/my_items")
    if models.Users.check_vip(message.from_user.id) is True:
        my_items = models.Items.user_items(message.from_user.id)
        answer = 'Ваши предметы:\n\n'
        for key in my_items:
            answer = answer + f"{key}: {my_items[key]}\n"
        await message.answer(answer, reply_markup=kb.inventory_kb)
    else:
        await message.answer("У вас нет доступа к этой команде")


# noinspection PyTypeChecker
@router.callback_query(F.data == "items_price")
async def items_price(callback: CallbackQuery):
    models.LogBase.add(callback.from_user.id, callback.from_user.username, "items_price")
    items = models.Items.user_items(callback.from_user.id)
    answer = 'Стоимость вашего инвентаря:\n\n'
    total = 0
    for key in items:
        item_price = sm.get_item(730, key, currency='RUB')
        x = str(item_price['lowest_price'])[:-5]
        x = x.replace(',', '.')
        multi_price = float(x) * items[key]
        total += multi_price
        answer = answer + f"{key}: {items[key]} * {item_price['lowest_price']} = {round(multi_price, 2)} руб.\n"
    answer = answer + f"\nСтоимость всего инвентаря: {round(total, 2)} руб.\n"
    answer = answer + f"\nСтоимость с учетом комиссии: {round(total * sell_fee, 2)} руб."
    await callback.message.answer(answer)


@router.message(F.text == "➕ADD ITEM➕")
async def add_item(message: Message, state: FSMContext):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/add_item")
    await message.answer(
        "Напишите название предмета на англ и через . кол-во\nПримеры написания:\nClutch Case.100\nFracture Case.10")
    await state.set_state(AddInventory.add_item_state)


@router.message(AddInventory.add_item_state, F.text)
async def add_item_bd(message: Message, state: FSMContext):
    mes = message.text.split(".")
    hash_name = mes[0]
    try:
        item_count = int(mes[1])
        telegram_id = message.from_user.id
        models.Items.add_item(telegram_id, hash_name, item_count)
        await message.answer(f"Вы добавили {hash_name}")
        await state.clear()
    except ValueError:
        await message.answer("Ошибка ввода")
        await state.clear()


@router.message(F.text == "❌DELETE❌")
async def delete_item(message: Message, state: FSMContext):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/delete")
    if models.Users.check_vip(message.from_user.id) is True:
        await message.answer("Введите название предмета.")
        await state.set_state(AddInventory.delete_item_state)
    else:
        await message.answer("У вас недостаточно прав.")


@router.message(AddInventory.delete_item_state, F.text)
async def delete_item_state(message: Message, state: FSMContext):
    models.Items.delete_item(message.from_user.id, message.text)
    await message.answer(f"Вы успешно удалили {message.text}")
    await state.clear()
