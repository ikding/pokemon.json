import pytest
from choose_pokemon import get_max_pogo_cp


iv_tol = 1
cp_tol = 10


def test_get_max_pogo_cp_pikachu():
    shinx_base = {
        "HP": 35,
        "Attack": 55,
        "Defense": 40,
        "Sp. Attack": 50,
        "Sp. Defense": 50,
        "Speed": 90,
    }
    pogo_attack, pogo_defense, pogo_hp, pogo_cp = get_max_pogo_cp(
        pokemon_base=shinx_base
    )

    assert abs(pogo_attack - 112) <= iv_tol
    assert abs(pogo_defense - 96) <= iv_tol
    assert abs(pogo_hp - 111) <= iv_tol
    assert abs(pogo_cp - 938) <= cp_tol
