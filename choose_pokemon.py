"""Random pokemon chooser."""
import json
import os
import random


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


def choose_pokemon(pokemon_dict: dict) -> dict:
    pokemon_idx = random.randint(1, 809)
    return pokemon_dict[pokemon_idx]


if __name__ == "__main__":
    pokemons = load_pokemon_file()
    pokemon = choose_pokemon(pokemon_dict=pokemons)
    print(json.dumps(pokemon, indent=4))
