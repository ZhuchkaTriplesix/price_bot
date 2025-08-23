from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from . import action
from .keyboard import owners_kb
from .schemas import TelegramIdPayload, DeleteItemPayload


router = Router()


class ChangeAccessState(StatesGroup):
    get_user_id_state = State()
    add_admin_id_state = State()
    delete_admin_state = State()
    del_item_state = State()


@router.message(F.text == "/admin")
async def admin_kb(message: Message):
    access = action.check_admin_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Админ меню", reply_markup=owners_kb)
    else:
        await message.answer(access.error)


@router.message(F.text == "/give_vip")
async def change_access(message: Message, state: FSMContext):
    access = action.check_admin_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Введите айди пользователя.")
        await state.set_state(ChangeAccessState.get_user_id_state)
    else:
        await message.answer(access.error)


@router.message(ChangeAccessState.get_user_id_state, F.text)
async def change_user_access(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        payload = TelegramIdPayload(telegram_id=telegram_id)
        answer = await action.give_vip(payload)
        await message.answer(answer)
        await state.clear()
    except ValueError:
        await message.answer("Неверный телеграм айди.")
        await state.clear()


@router.message(F.text == "/kill")
async def kill_process(message: Message):
    access = action.check_owner_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Отключаюсь(..")
        raise SystemExit(0)
    else:
        await message.answer(access.error)


@router.message(F.text == "/add_admin")
async def add_admin(message: Message, state: FSMContext):
    access = action.check_owner_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Введите айди пользователя.")
        await state.set_state(ChangeAccessState.add_admin_id_state)
    else:
        await message.answer(access.error)


@router.message(ChangeAccessState.add_admin_id_state, F.text)
async def add_admin_state(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        payload = TelegramIdPayload(telegram_id=telegram_id)
        answer = await action.add_admin(payload)
        await message.answer(answer)
        await state.clear()
    except ValueError:
        await message.answer("Неверный телеграм айди.")
        await state.clear()


@router.message(F.text == "/delete_admin")
async def delete_admin(message: Message, state: FSMContext):
    access = action.check_owner_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Введите айди пользователя.")
        await state.set_state(ChangeAccessState.delete_admin_state)
    else:
        await message.answer(access.error)


@router.message(ChangeAccessState.delete_admin_state, F.text)
async def delete_admin_state(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        payload = TelegramIdPayload(telegram_id=telegram_id)
        answer = await action.delete_admin(payload)
        await message.answer(answer)
        await state.clear()
    except ValueError:
        await message.answer("Неверный телеграм айди.")
        await state.clear()


@router.message(F.text == "/admin_list")
async def admin_list(message: Message):
    access = action.check_admin_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Список Админов недоступен без сервиса БД.")
    else:
        await message.answer(access.error)


@router.message(F.text == "/del_item")
async def del_item(message: Message, state: FSMContext):
    access = action.check_admin_access(message.from_user.id)
    if access.is_allowed:
        await message.answer("Введите айди.хешнейм")
        await state.set_state(ChangeAccessState.del_item_state)
    else:
        await message.answer(access.error)


@router.message(ChangeAccessState.del_item_state, F.text)
async def del_item_state(message: Message, state: FSMContext):
    mes = message.text.split(".")
    if len(mes) != 2:
        await message.answer("Неверный ввод.")
        await state.clear()
        return
    hash_name = mes[1]
    try:
        telegram_id = int(mes[0])
        payload = DeleteItemPayload(telegram_id=telegram_id, hash_name=hash_name)
        answer = await action.delete_item(payload)
        await message.answer(answer)
        await state.clear()
    except ValueError:
        await message.answer("Неверный ввод.")
        await state.clear()


