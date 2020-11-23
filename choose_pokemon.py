"""Random pokemon chooser."""
import json
import os
import random
from math import floor, sqrt
from typing import Dict

from PIL import Image


def load_pokemon_file() -> dict:
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokedex.json")
    with open(fpath) as f:
        pokemon_json = json.load(f)

    pokemon_dict = {}
    for pokemon in pokemon_json:
        pokemon_dict[pokemon["id"]] = {
            "name": pokemon["name"]["english"],
            "type": pokemon["type"],
            "base": pokemon["base"],
        }

    return pokemon_dict


def get_max_dpogo_cp(pokemon_base: Dict[str, int]) -> int:
    max_iv = 15
    cp_modifier = 0.7903
    attacks = [pokemon_base["Attack"], pokemon_base["Sp. Attack"]]
    defenses = [pokemon_base["Defense"], pokemon_base["Sp. Defense"]]

    pogo_speed = 1 + ((pokemon_base["Speed"] - 75) / 500)
    pogo_attack = (
        round(round(2 * (7 * max(attacks) / 8 + min(attacks) / 8)) * pogo_speed)
        + max_iv
    )
    pogo_defense = (
        round(round(2 * (7 * max(defenses) / 8 + min(defenses) / 8)) * pogo_speed)
        + max_iv
    )
    pogo_hp = (pokemon_base["HP"] + max_iv) * 2 + max_iv
    pogo_cp = floor(
        max(
            [
                10,
                (
                    pogo_attack
                    * sqrt(pogo_defense)
                    * sqrt(pogo_hp)
                    * cp_modifier ** 2
                    / 10
                ),
            ]
        )
    )

    return pogo_attack, pogo_defense, pogo_hp, pogo_cp


def choose_pokemon(pokemon_dict: dict) -> dict:
    pokemon_idx = random.choice(list(pokemon_dict.keys()))
    return pokemon_idx, pokemon_dict[pokemon_idx]


if __name__ == "__main__":
    pokemons = load_pokemon_file()
    pokemon_idx, pokemon = choose_pokemon(pokemon_dict=pokemons)
    pokemon_cp = get_max_dpogo_cp(pokemon_base=pokemon["base"])
    print(
        f"index: {pokemon_idx}\n"
        f'name: {pokemon["name"]}\n'
        f"CP: {pokemon_cp}\n"
        f'type: {pokemon["type"]}'
    )
    image = Image.open(os.path.join("images", f"{str(pokemon_idx).zfill(3)}.png"))
    image.show()
