import requests
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/galaxies', methods=['GET'])
def get_galaxies():
    url = "https://images-api.nasa.gov/search"
    params = {
        "q": "galaxy",
        "media_type": "image",
    }

    response = requests.get(url, params=params)
    data = response.json()

    galaxies = []
    for item in data["collection"]["items"]:
        galaxy = {
            "title": item["data"][0]["title"],
            "description": item["data"][0]["description"],
            "image_url": item["links"][0]["href"]
        }
        galaxies.append(galaxy)

    return jsonify(galaxies)

if __name__ == "__main__":
    app.run(debug=True)
