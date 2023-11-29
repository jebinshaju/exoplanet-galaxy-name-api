from flask import Flask, jsonify
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

exoplanet_data = []
galaxy_data = []




@app.route('/exoplanets', methods=['GET'])
def get_random_exoplanet():
    if not exoplanet_data:
        return jsonify({'error': 'Exoplanet data is empty'})
    
    exoplanet_name = exoplanet_data.pop()
    
    # Fetch images related to the exoplanet using NASA Images API
    search_query = f"exoplanet {exoplanet_name}"
    nasa_api_url = f"https://images-api.nasa.gov/search?q={search_query}&media_type=image&page_size=1&page=1"
    
    try:
        response = requests.get(nasa_api_url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and data['items']:
                image_url = data['items'][0]['links']['href']
            else:
                image_url = "No image available"
        else:
            image_url = "Error fetching image"
    except Exception as e:
        image_url = "Error fetching image"

    exoplanet_info = extract_exoplanet_details(exoplanet_name)
    exoplanet_info['image_url'] = image_url

    return jsonify(exoplanet_info)

@app.route('/galaxies', methods=['GET'])
def get_random_galaxy():
    if not galaxy_data:
        fetch_and_shuffle_galaxy_data()
    random_galaxy = random.choice(galaxy_data)
    return jsonify(random_galaxy)

if __name__ == '__main__':
   
    
    # Run the Flask app
    app.run(debug=True)
