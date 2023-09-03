from typing import List
import json

HISTORY_SIZE = 64
STORAGE_SHINIES_KEY = "shinies"

# The last HISTORY_SIZE sets of Pokémon to be generated, newest first.
latest_pokemon: List[List[GeneratedPokemon]] = []

displayed_index: int = -1  # Nothing displayed on first load

def add_to_history(pokemon: List[GeneratedPokemon]):
    latest_pokemon.insert(0, pokemon)
    while len(latest_pokemon) > HISTORY_SIZE:
        latest_pokemon.pop()

    shinies = get_shinies()
    shinies.insert(0, [p for p in pokemon if p.shiny])
    localStorage_set(STORAGE_SHINIES_KEY, json.dumps(shinies))

    displayed_index = 0
    toggle_history_visibility(shinies)

def toggle_history_visibility(shinies=None):
    previous_element = document.getElementById("previous")
    next_element = document.getElementById("next")
    shinies = shinies or get_shinies()
    shiny_count_element = document.getElementById("shiny-count")
    shinies_element = document.getElementById("shinies")
    shiny_toggler_element = document.getElementById("shiny-toggler")
    
    previous_element.classList.toggle("hidden", displayed_index >= len(latest_pokemon) - 1)
    next_element.classList.toggle("hidden", displayed_index <= 0)
    
    shiny_count_element.innerHTML = str(len(shinies))
    shinies_element.innerHTML = ''.join([p.to_image() for p in shinies])
    shiny_toggler_element.classList.toggle("invisible", len(shinies) == 0)

def display_previous():
    display_history_at_index(displayed_index + 1)  # One older

def display_next():
    display_history_at_index(displayed_index - 1)  # One newer

def display_history_at_index(index: int):
    index = max(0, min(index, len(latest_pokemon) - 1))
    displayed_index = index
    display_pokemon(latest_pokemon[index])
    toggle_history_visibility()

# All encountered shiny Pokémon, newest first.
def get_shinies():
    shinies = json.loads(localStorage_get(STORAGE_SHINIES_KEY))
    if not isinstance(shinies, list):
        return []
    return [GeneratedPokemon.from_json(shiny) for shiny in shinies]

def toggle_shiny_display():
    is_invisible = document.getElementById("shiny-container").classList.toggle("invisible")
    update_shiny_toggler(not is_invisible)

def update_shiny_toggler(shinies_visible: bool):
    button = document.getElementById("shiny-toggler")
    button.classList.toggle("is-hiding", not shinies_visible)
    button.classList.toggle("is-showing", shinies_visible)

def clear_shinies():
    if window.confirm("Are you sure you want to clear your shiny Pokémon?"):
        localStorage_remove(STORAGE_SHINIES_KEY)
        document.getElementById("shiny-container").classList.add("invisible")
        toggle_history_visibility([])
        update_shiny_toggler(False)  # Prepare for next time
