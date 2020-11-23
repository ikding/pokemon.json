"""Random pokemon chooser.

It will choose a random pokemon from the ``pokedex.json`` and show its number, name,
combat power (CP) in Pokemon Go, and its type.

To run::
    python choose_pokemon.py
"""
import json
import os
import random
from math import floor, sqrt
from typing import Dict, Sequence, Tuple

from PIL import Image


def load_pokemon_file() -> dict:
    """Load pokemon stats from the ``pokedex.json`` file in the same folder.

    Returns:
        dict: Pokemon information, keyed by pokemon index (int)
    """
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


def calculate_pogo_stats(
    pokemon_base: Dict[str, int],
    max_iv: int = 15,
    cp_modifier: float = 0.7903001,
    cp_ceiling: int = 4000,
    cp_nerf: float = 0.91,
) -> Sequence[int]:
    """Calculate pokemon go stats in Pokemon Go.

    Args:
        pokemon_base (Dict[str, int]): Pokemon stats from the main series game.
            This information is available from the ``pokedex.json`` file.
        max_iv (int, optional): Max individual IV in Pokemon go. Defaults to 15.
        cp_modifier (float, optional): CP modifier for Pokemon Go.
            Defaults to 0.7903001.
        cp_ceiling (int, optional): Ceiling of CP in Pokemon Go. Defaults to 4000.
        cp_nerf (float, optional): Nerfing factor of CP in Pokemon Go. This is only
            applied to pokemon with CP over cp_ceiling. Defaults to 0.91.

    Returns:
        Sequence[int]: Tuple of 4 integers: base attack, base defense, base HP,
            and maximum CP in Pokemon Go for the stats.
    """
    attacks = [pokemon_base["Attack"], pokemon_base["Sp. Attack"]]
    defenses = [pokemon_base["Defense"], pokemon_base["Sp. Defense"]]

    pogo_speed = 1 + ((pokemon_base["Speed"] - 75) / 500)
    pogo_attack = (
        round(round(2 * (7 * max(attacks) / 8 + 1 * min(attacks) / 8)) * pogo_speed)
        + max_iv
    )
    pogo_defense = (
        round(round(2 * (5 * max(defenses) / 8 + 3 * min(defenses) / 8)) * pogo_speed)
        + max_iv
    )
    pogo_hp = floor(pokemon_base["HP"] * 1.75 + 50) + max_iv
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

    if pogo_cp >= cp_ceiling:
        pogo_cp = round(pogo_cp * cp_nerf)

    return pogo_attack - max_iv, pogo_defense - max_iv, pogo_hp - max_iv, pogo_cp


def choose_pokemon(pokemon_dict: dict) -> Tuple[int, dict, dict]:
    """Randomly choose a pokemon and return its attributes.

    The attributes we return include:
    * pokemon_idx: int index of the randomly chosen pokemon.
    * pokemon: a dict of pokemon attributes which include name, base stats, and type.
    * pokemon_stats: a dict of pokemon stats.

    Args:
        pokemon_dict (dict): pokemon dict from :py:func:`choose_pokemon.load_pokemon_file`.

    Returns:
        Tuple[int, dict, dict]: tuple of pokemon attributes. The attributes we return include:

        * pokemon_idx: int index of the randomly chosen pokemon.
        * pokemon: a dict of pokemon attributes which include name, base stats, and type.
        * pokemon_stats: a dict of pokemon stats.
    """
    pokemon_idx = random.choice(list(pokemon_dict.keys()))
    pokemon = pokemon_dict[pokemon_idx]
    pokemon_stats_list = calculate_pogo_stats(pokemon_base=pokemon["base"])
    pokemon_stats = dict(zip(["ATK", "DEF", "STA", "CP"], pokemon_stats_list))
    return pokemon_idx, pokemon, pokemon_stats


if __name__ == "__main__":
    pokemons = load_pokemon_file()
    pokemon_idx, pokemon, pokemon_stats = choose_pokemon(pokemon_dict=pokemons)
    print(
        f"index: {pokemon_idx}\n"
        f'name: {pokemon["name"]}\n'
        f'type: {pokemon["type"]}\n'
        f"stats: {pokemon_stats}"
    )
    image = Image.open(os.path.join("images", f"{str(pokemon_idx).zfill(3)}.png"))
    image.show()
