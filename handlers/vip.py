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


@router.message(F.text == "/support")
async def support(message: Message):
    if models.check_access(message.from_user.id) in ("Vip", "Admin", "Owner"):
        await message.answer("Напишите - @ZhuchkaTriplesix")
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(F.text == "/vip_help")
async def vip_help(message: Message):
    await message.answer("Команды для Vip пользователей:\n/support - Персональная помощь с ботом")
