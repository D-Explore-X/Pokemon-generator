import json

def fix_json(json_str):
    try:
        # Attempt to load the JSON
        data = json.loads(json_str)
        # Dump and return the correctly formatted JSON
        return json.dumps(data, indent=4)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

# Read the JSON file
file_path = r'I:\Python\D Explorex\Pokemon-generator\updated code pro\hisui_updated.json'
with open(file_path, 'r') as json_file:
    json_content = json_file.read()

# Attempt to fix the JSON
fixed_json = fix_json(json_content)

# If the JSON was successfully fixed, write it back to the file
if fixed_json is not None:
    with open(file_path, 'w') as json_file:
        json_file.write(fixed_json)
        print("JSON file fixed and saved.")
