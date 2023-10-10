from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext

json_data = "user_list.json"
push_data = "users_time.json"
admins = "admins.json"
router = Router()
vip_id = []


class VipStatusState(StatesGroup):
    change_vip_state = State()
    change_vip_callback_state = State()
    vip_add_state = State()
    vip_delete_state = State()


@router.message(F.text == "/check_vip")
async def vip_status(message: Message):
    user_id = f"{message.from_user.id}"
    data = json_support.read_inf(admins)
    vip_status_time = "01-01-2024"
    if user_id not in data.keys():
        await message.answer("У вас нет вип статуса.")
    else:
        await message.answer(f"Ваш вип статус будет активен до {vip_status_time}")


@router.message(F.text == "/change_vip")
async def change_vip(message: Message, state: FSMContext):
    user_id = f"{message.from_user.id}"
    data = json_support.read_inf(admins)
    if user_id in data.keys():
        if data[user_id] not in ("Owner", "Admin", "Kurator"):
            await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")
        else:
            await message.answer("Введите телеграм айди пользователя")
            await state.set_state(VipStatusState.change_vip_state)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(VipStatusState.change_vip_state, F.text)
async def change_vip_state(message: Message):
    user_id = f"{message.text}"
    vip_id.append(user_id)
    await message.answer("Что хотите сделать?", reply_markup=kb.vip_change_kb)


@router.callback_query(F.data == "vip_add")
async def vip_add(callback: CallbackQuery, state: FSMContext):
    vip_status_time = "01-01-2024"
    data = json_support.read_inf(admins)
    user_id = vip_id[0]
    c = {user_id: ["Vip", vip_status_time]}
    data.update(c)
    json_support.write_inf(data, admins)
    await callback.message.delete()
    await callback.message.answer(f"Пользователю {user_id} был выдан вип доступ до {vip_status_time}.")
    vip_id.clear()
    await state.clear()


@router.callback_query(F.data == "vip_delete")
async def vip_delete(callback: CallbackQuery, state: FSMContext):
    data = json_support.read_inf(admins)
    user_id = vip_id[0]
    if user_id not in data.keys():
        await callback.message.delete()
        await callback.message.answer(f"Пользователь {user_id}, не имеет вип доступа")
    else:
        if data[user_id] not in ("Owner", "Kurator", "Admin"):
            del data[user_id]
            json_support.write_inf(data, admins)
            await callback.message.delete()
            await callback.message.answer(f"Вы удалили вип доступ у пользователя {user_id}.")
        else:
            await callback.message.delete()
            await callback.message.answer(f"У вас недостаточно прав для редактирования группы пользователя {user_id}.")
    vip_id.clear()
    await state.clear()


@router.message(F.text == "/vip_list")
async def vip_list(message: Message):
    user_id = f"{message.from_user.id}"
    data = json_support.read_inf(admins)
    if user_id not in data.keys():
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")
    else:
        x = ''
        for vip in data:
            status = data[vip]
            x = f"{x + vip}: {status} \n"
        await message.answer(x)
