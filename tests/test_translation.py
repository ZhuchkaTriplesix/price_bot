import pytest

from bot.src.misc.translation import translate_case_name_to_russian


@pytest.mark.parametrize(
    "src,expected",
    [
        ("CS:GO Weapon Case", "Оружейный кейс CS:GO"),
        ("Revolution Case", "Revolution Case"),
        ("Unknown", "Unknown"),
    ],
)
def test_translate_case_name_to_russian(src, expected):
    assert translate_case_name_to_russian(src) == expected


