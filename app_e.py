from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__)

# Load Pokémon data from JSON files

data_dir = "data/"
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
    return render_template('index.html', options=current_options)

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
        if (current_options["legendaries"] or not pokemon["isLegendary"]) \
            and (current_options["nfes"] or not pokemon["isNfe"]):
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

    return jsonify({
        "pokemon": selected_pokemon,
        "sprite_urls": sprite_urls
    })

def get_sprite_url(pokemon):
    sprite_dir = "pokemon_sprites"
    sprite_type = "normal"
    sprite_suffix = ""
    
    if current_options["sprites"]:
        sprite_type = "shiny" if "shiny" in current_options else "normal"
    
    # Construct the sprite file name based on Pokémon name
    sprite_filename = f"{pokemon['name'].lower()}{sprite_suffix}.png"
    
    # Define the sprite path relative to the "static" folder
    sprite_path = os.path.join(sprite_dir, sprite_type, sprite_filename)
    
    # Construct the URL using Flask's send_from_directory
    sprite_url = app.config['SITE_URL'] + sprite_path
    
    return sprite_url

if __name__ == '__main__':
    app.config['SITE_URL'] = "http://localhost:5000"
    app.run(debug=True)
