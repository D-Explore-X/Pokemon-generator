from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Define a default set of options
DEFAULT_OPTIONS = {
    "n": 6,
    "region": "all",
    "type": "all",
    "legendaries": True,
    "nfes": True,
    "sprites": True,
    "natures": False,
    "forms": True,
    "generate": False
}

# Store the options globally
current_options = DEFAULT_OPTIONS

@app.route('/')
def index():
    global current_options
    # Load options from query parameters
    options = request.args.to_dict()
    
    # Update the global options with the new values
    for key, value in options.items():
        if key in current_options:
            current_options[key] = value
    
    # Render the template with the current options
    return render_template('index.html', options=current_options)

@app.route('/options', methods=['GET', 'POST'])
def options():
    global current_options
    if request.method == 'POST':
        # Load options from the POST request
        options = request.form.to_dict()
        # Update the global options with the new values
        for key, value in options.items():
            if key in current_options:
                current_options[key] = value
        
        # Persist the options to a file or database if needed
        with open('options.json', 'w') as f:
            json.dump(current_options, f)
        
    return json.dumps(current_options)

if __name__ == '__main__':
    app.run()
