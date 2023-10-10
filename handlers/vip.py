from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext

json_data = "user_list.json"
push_data = "users_time.json"
admins = "admins.json"
router = Router()


class VipStatusState(StatesGroup):
    change_vip_state = State()
    change_vip_callback_state = State()


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
async def change_vip_state(message: Message, state: FSMContext):
    pass
