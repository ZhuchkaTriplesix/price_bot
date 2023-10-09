from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import sys

json_data = "user_list.json"
push_data = "users_time.json"
admins = "admins.json"
router = Router()
admins_id = []


class AdminAddStatus(StatesGroup):
    id_add = State()
    group_change = State()
    delete_admin = State()
    group_change_callback = State()


@router.message(F.text == "/admin")
async def admin_menu(message: Message):
    admin_data = json_support.read_inf(admins)
    user_id = f"{message.from_user.id}"
    if user_id in admin_data.keys():
        if admin_data[user_id] not in "Owner":
            await message.answer("Админ меню", reply_markup=kb.admins_kb)
        else:
            await message.answer("Админ меню", reply_markup=kb.owners_kb)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(F.text == "/kill")
async def kill_process(message: Message):
    admin_data = json_support.read_inf(admins)
    user_id = f"{message.from_user.id}"
    if user_id in admin_data.keys():
        await message.answer("Вы вырубили бота")
        sys.exit()
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(F.text == '/add_admin')
async def add_admin(message: Message, state: FSMContext):
    admin_data = json_support.read_inf(admins)
    user_id = f"{message.from_user.id}"
    if user_id in admin_data.keys():
        if admin_data[user_id] not in "Owner":
            await message.answer("У вас недостаточно прав")
        else:
            await message.answer("Введите телеграм айди пользователя")
            await state.set_state(AdminAddStatus.id_add)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(AdminAddStatus.id_add, F.text)
async def id_add(message: Message):
    user_id = message.text
    data = json_support.read_inf(admins)
    us = {user_id: "Admin"}
    data.update(us)
    json_support.write_inf(data, admins)
    await message.answer(f"Вы выдали админ доступ {user_id}")


@router.message(F.text == "/back")
async def main_menu_back(message: Message):
    await message.answer("Основное меню", reply_markup=kb.main)


@router.message(F.text == "/admin_list")
async def admin_list(message: Message):
    x = ''
    user_id = f"{message.from_user.id}"
    admin_data = json_support.read_inf(admins)
    if user_id in admin_data.keys():
        for admin in admin_data:
            status = admin_data[admin]
            x = f"{x + admin}: {status} \n"
        await message.answer(x)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(F.text == "/delete_admin")
async def delete_admin(message: Message, state: FSMContext):
    user_id = f"{message.from_user.id}"
    admin_data = json_support.read_inf(admins)
    if user_id in admin_data.keys():
        if admin_data[user_id] not in "Owner":
            await message.answer("У вас недостаточно прав")
        else:
            await message.answer("Введите телеграм айди пользователя")
            await state.set_state(AdminAddStatus.delete_admin)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(F.text == "/change_group")
async def change_group(message: Message, state: FSMContext):
    data = json_support.read_inf(admins)
    user_id = f"{message.from_user.id}"
    if user_id in data.keys():
        if data[user_id] not in "Owner":
            await message.answer("У вас недостаточно прав")
        else:
            await message.answer("Введите телеграм айди пользователя")
            await state.set_state(AdminAddStatus.group_change)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(AdminAddStatus.group_change, F.text)
async def change_status(message: Message, state: FSMContext):
    admins_id.append(message.text)
    await message.answer("На какую группу, вы хотите поменять?", reply_markup=kb.change_status_kb)
    await state.set_state(AdminAddStatus.group_change_callback)


@router.callback_query(AdminAddStatus.group_change_callback, F.data == "Kurator")
async def change_group_callback(callback: CallbackQuery):
    admin_id = admins_id[0]
    data = json_support.read_inf(admins)
    group = callback.data
    user_group = {admin_id: group}
    data.update(user_group)
    json_support.write_inf(data, admins)
    await callback.message.delete()
    await callback.message.answer(f"Вы поменяли группу администратора {admin_id} на {group}")
    admins_id.clear()


@router.callback_query(AdminAddStatus.group_change_callback, F.data == "Owner")
async def change_group_callback(callback: CallbackQuery):
    admin_id = admins_id[0]
    data = json_support.read_inf(admins)
    group = callback.data
    user_group = {admin_id: group}
    data.update(user_group)
    json_support.write_inf(data, admins)
    await callback.message.delete()
    await callback.message.answer(f"Вы поменяли группу администратора {admin_id} на {group}")
    admins_id.clear()


@router.message(AdminAddStatus.delete_admin, F.text)
async def id_add(message: Message):
    user_id = message.text
    data = json_support.read_inf(admins)
    del data[user_id]
    json_support.write_inf(data, admins)
    await message.answer(f"Вы убрали админ доступ у {user_id}")
