from __future__ import annotations

from typing import Dict


_EN_TO_RU_CASES: Dict[str, str] = {
    "CS:GO Weapon Case": "Оружейный кейс CS:GO",
    "eSports 2013 Case": "eSports 2013 Case",
    "Operation Bravo Case": "Кейс операции «Браво",
    "CS:GO Weapon Case 2": "Оружейный кейс CS:GO #2",
    "eSports 2013 Winter Case": "eSports 2013 Winter Case",
    "Winter Offensive Weapon Case": "Оружейный кейс «Winter Offensive»",
    "CS:GO Weapon Case 3": "Оружейный кейс CS:GO #3",
    "Operation Phoenix Weapon Case": "Оружейный кейс операции «Феникс»",
    "Huntsman Weapon Case": "Охотничий оружейный кейс",
    "Operation Breakout Weapon Case": "Оружейный кейс операции «Прорыв»",
    "eSports 2014 Summer Case": "eSports 2014 Summer Case",
    "Operation Vanguard Weapon Case": "Оружейный кейс операции «Авангард»",
    "Chroma Case": "Хромированный кейс",
    "Chroma 2 Case": "Хромированный кейс #2",
    "Falchion Case": "Кейс «Фальшион»",
    "Revolver Case": "Револьверный кейс",
    "Shadow Case": "Тёмный кейс",
    "Operation Wildfire Case": "Кейс операции «Дикое пламя»",
    "Chroma 3 Case": "Хромированный кейс #3",
    "Gamma Case": "Гамма-кейс",
    "Gamma 2 Case": "Гамма-кейс #2",
    "Glove Case": "Перчаточный кейс",
    "Spectrum Case": "Кейс «Спектр»",
    "Operation Hydra Case": "Кейс операции «Гидра»",
    "Spectrum 2 Case": "Кейс «Спектр 2»",
    "Clutch Case": "Кейс «Решающий момент»",
    "Horizon Case": "Кейс «Горизонт»",
    "Danger Zone Case": "Кейс «Запретная зона»",
    "Prisma Case": "Кейс «Призма»",
    "CS20 Case": "Кейс «CS20»",
    "Shattered Web Case": "Кейс «Расколотая сеть»",
    "Prisma 2 Case": "Кейс «Призма 2»",
    "Fracture Case": "Кейс «Разлом»",
    "Operation Broken Fang Case": "Кейс операции «Сломанный клык»",
    "Snakebite Case": "Кейс «Змеиный укус»",
    "Operation Riptide Case": "Кейс операции «Хищные воды»",
    "Dreams & Nightmares Case": "Кейс «Грёзы и кошмары»",
    "Recoil Case": "Recoil Case",
    "Revolution Case": "Revolution Case",
}


def translate_case_name_to_russian(english_name: str) -> str:
    return _EN_TO_RU_CASES.get(english_name, english_name)
