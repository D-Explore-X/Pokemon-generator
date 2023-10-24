from flask import Flask, render_template, request, jsonify
import json
import random

import os

app = Flask(__name__)

# Load Pokémon data from JSON files

data_dir = "data_updated/"
regions = [
    "all.json",
    "alola_usum.json",
    "alola.json",
    "galar.json",
    "hisui.json",
    "hoenn.json",
    "johto.json",
    "kalos.json",
    "kanto.json",
    "paldea.json",
    "sinnoh.json",
    "sinnoh_pt.json",
    "unova.json",
    "unova_b2w2.json",
]

pokemon_data = {}
for region in regions:
    with open(data_dir + region, "r") as json_file:
        region_data = json.load(json_file)
        pokemon_data[region.split(".")[0]] = region_data

# Define a default set of options
DEFAULT_OPTIONS = {
    "n": 1,
    "region": "alola",
    "type": "normal",
    "legendaries": False,
    "nfes": False,
    "sprites": True,
    "natures": False,
    "forms": False,
}

# Store the options globally
current_options = DEFAULT_OPTIONS

@app.route('/')
def index():
    return render_template('indexxxx.html', options=current_options)

# ...

@app.route('/generate', methods=['POST'])
def generate_pokemon():
    global current_options
    options = request.form.to_dict()
    current_options.update(options)

    # Load Pokémon data based on the selected region
    selected_region = pokemon_data.get(current_options["region"], [])

    # Filter Pokémon based on options
    eligible_pokemon = []
    for pokemon in selected_region:
        # Check if the 'types' key exists in the pokemon dictionary
        if (
            (current_options["legendaries"] or not pokemon.get("isLegendary", False)) and
            (current_options["nfes"] or not pokemon.get("isNfe", False)) and
            (
                current_options["type"] == "all" or
                ("types" in pokemon and current_options["type"] in pokemon["types"])
            )
        ):
            eligible_pokemon.append(pokemon)

    # Randomly select N Pokémon
    num_pokemon = int(current_options["n"])
    if num_pokemon > len(eligible_pokemon):
        num_pokemon = len(eligible_pokemon)
    selected_pokemon = random.sample(eligible_pokemon, num_pokemon)

    # Get sprite URLs for selected Pokémon
    sprite_urls = []
    if current_options["sprites"]:
        sprite_urls = [get_sprite_url(pokemon) for pokemon in selected_pokemon]

    # Prepare data to send to the client
    response_data = {
        "pokemon": selected_pokemon,
        "sprite_urls": sprite_urls,
    }

    # If "forms" option is selected, include forms data in the response
    if current_options["forms"]:
        forms = []
        for pokemon in selected_pokemon:
            if "forms" in pokemon:
                forms.extend(pokemon["forms"])
        response_data["forms"] = forms
    for pokemon in selected_pokemon:
        if "desc" in pokemon:
            response_data.setdefault("desc", []).append(pokemon["desc"])

    return jsonify(response_data)
def get_sprite_url(pokemon):
    sprite_dir = "static/pokemon_sprites"
    sprite_type = "normal"
    sprite_suffix = ""
    
    # Check if "sprites" option is selected
    if current_options["sprites"]:
        sprite_type = "shiny" if "shiny" in current_options else "normal"
    
        # Construct the sprite file name based on Pokémon name
        sprite_filename = f"{pokemon['name'].lower()}{sprite_suffix}.png"
    
        # Define the sprite path relative to the "static" folder
        sprite_path = os.path.join(sprite_dir, sprite_type, sprite_filename)
    
        # Construct the URL using Flask's send_from_directory
        sprite_url = sprite_path
    else:
        # If "sprites" option is not selected, set sprite_url to an empty string
        sprite_url = ""
    
    return sprite_url


if __name__ == '__main__':
    app.config['SITE_URL'] = "http://localhost:5000"
    app.run(debug=True)
