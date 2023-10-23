from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import sys
import models

router = Router()


class ChangeAccessState(StatesGroup):
    get_user_id_state = State()
    add_admin_id_state = State()
    delete_admin_state = State()


@router.message(F.text == "/admin")
async def admin_kb(message: Message):
    if models.check_admin(message.from_user.id) is True:
        await message.answer("Админ меню", reply_markup=kb.owners_kb)


@router.message(F.text == "/give_vip")
async def change_access(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if models.check_admin(telegram_id) is True:
        await message.answer("Введите айди пользователя")
        await state.set_state(ChangeAccessState.get_user_id_state)
    else:
        await message.answer("У вас нет доступа к этой команде.")


@router.message(ChangeAccessState.get_user_id_state, F.text)
async def change_user_access(message: Message, state: FSMContext):
    telegram_id = message.text
    telegram_id = int(telegram_id)
    models.change_access(telegram_id, 1)
    await message.answer("Вы успешно поменяли группу пользователя, на Vip")
    await state.clear()


@router.message(F.text == "/check_access")
async def check_access(message: Message):
    await message.answer(models.check_access(message.from_user.id))


@router.message(F.text == "/kill")
async def kill_process(message: Message):
    if models.check_admin(message.from_user.id) is True:
        await message.answer("Отключаюсь(..")
        sys.exit()
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(F.text == "/add_admin")
async def add_admin(message: Message, state: FSMContext):
    if models.check_admin(message.from_user.id) is True:
        await message.answer("Введите айди пользователя")
        await state.set_state(ChangeAccessState.add_admin_id_state)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(ChangeAccessState.add_admin_id_state, F.text)
async def add_admin_state(message: Message, state: FSMContext):
    telegram_id = int(message.text)
    models.change_access(telegram_id, "Admin")
    await message.answer("Вы выдали админ доступ пользователю")
    await state.clear()


@router.message(F.text == "/delete_admin")
async def delete_admin(message: Message, state: FSMContext):
    if models.check_admin(message.from_user.id) is True:
        await message.answer("Введите айди пользователя")
        await state.set_state(ChangeAccessState.delete_admin_state)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(ChangeAccessState.delete_admin_state, F.text)
async def delete_admin_state(message: Message, state: FSMContext):
    telegram_id = message.text
    models.change_access(telegram_id, "User")
    await message.answer("Вы удалили админ доступ у пользователя")
    await state.clear()


@router.message(F.text == "/admin_list")
async def admin_list(message: Message):
    owners = models.session.query(models.Users).where(models.Users.user_group == 3)
    admins = models.session.query(models.Users).where(models.Users.user_group == 2)
    bot_message = 'Список Админов:\n'
    for admin in owners:
        x = f"@{admin.nickname}: {admin.telegram_id} Owner\n"
        bot_message += x
    for admin in admins:
        x = f"@{admin.nickname}: {admin.telegram_id} Admin\n"
        bot_message += x
    await message.answer(bot_message)
