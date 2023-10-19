import asyncio
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from data import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import steammarket as sm

router = Router()


@router.message(F.text == "/support")
async def support(message: Message):
    await message.answer("@ZhuchkaTriplesix")
