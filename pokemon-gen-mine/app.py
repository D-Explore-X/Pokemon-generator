from flask import Flask, render_template, request, jsonify
import json
import random

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
    selected_region = pokemon_data[current_options["region"]]

    # Filter Pokémon based on options
    eligible_pokemon = []
    for pokemon in selected_region:
        if (current_options["legendaries"] or not pokemon["isLegendary"]) \
            and (current_options["nfes"] or not pokemon["isNfe"]):
            eligible_pokemon.append(pokemon)

    # Randomly select N Pokémon
    selected_pokemon = random.sample(eligible_pokemon, int(current_options["n"]))

    return jsonify(selected_pokemon)

if __name__ == '__main__':
    app.run(debug=True)
