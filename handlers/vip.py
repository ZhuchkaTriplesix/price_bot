import asyncio
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from data import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import steammarket as sm
import models

router = Router()


class AddChangeSteamId(StatesGroup):
    change_steam_id_state = State()


@router.message(F.text == "/support")
async def support(message: Message):
    if models.check_access(message.from_user.id) in ("Vip", "Admin", "Owner"):
        await message.answer("Напишите - @ZhuchkaTriplesix")
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(F.text == "/vip_help")
async def vip_help(message: Message):
    await message.answer(
        "Команды для Vip пользователей:\n/support - Персональная помощь с ботом\n/steam_id - поменять стим айди (по умолчанию его нет)")


@router.message(F.text == "/steam_id")
async def change_steam_id(message: Message, state: FSMContext):
    if models.check_access(message.from_user.id) in ("Vip", "Admin", "Owner"):
        await message.answer("Введите свой стим айди")
        await state.set_state(AddChangeSteamId.change_steam_id_state)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(AddChangeSteamId.change_steam_id_state, F.text)
async def change_steam_id_state(message: Message, state: FSMContext):
    steam_id = message.text
    try:
        steam_id = int(steam_id)
        models.change_steam_id(message.from_user.id, steam_id)
        await message.answer("Вы успешно изменили стим айди")
        await state.clear()
    except TypeError:
        await message.answer("Вы ввели неверный стим айди")
        await state.clear()
    except ValueError:
        await message.answer("Вы ввели неверный стим айди")
        await state.clear()
