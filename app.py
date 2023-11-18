from collections import deque
from flask import Flask, jsonify, request
import random
import json

app = Flask(__name__)

def load_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

exoplanets = load_json('exoplanets.json')
galaxies = load_json('galaxies_data.json')

recent_items = deque(maxlen=20)

@app.route('/shuffle', methods=['GET'])
def shuffle():
    while True:
        data = random.choice([exoplanets, galaxies])
        item = random.choice(data)
        if item not in recent_items:
            recent_items.append(item)
            return jsonify(data=item)

@app.route('/exoplanets', methods=['GET'])
def get_exoplanets():
    return jsonify(data=exoplanets)

@app.route('/galaxies', methods=['GET'])
def get_galaxies():
    return jsonify(data=galaxies)

if __name__ == '__main__':
    app.run(debug=True)
