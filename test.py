from flask import Flask, jsonify
import random
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

exoplanet_data = []
galaxy_data = []

def fetch_and_shuffle_exoplanet_data():
    table = NasaExoplanetArchive.query_criteria(table="PS", select="pl_name")
    exoplanet_data.extend([row['pl_name'] for row in table])
    random.shuffle(exoplanet_data)

def fetch_and_shuffle_galaxy_data():
    url = "https://en.wikipedia.org/wiki/List_of_galaxies"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", class_="wikitable")
        galaxy_data.clear()

        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if len(columns) >= 5:
                image_column = columns[0].find("img")
                original_url = image_column["src"] if image_column else "No image available"

                if "70px-" in original_url:
                    original_url = original_url.replace("70px-", "")
                parts = original_url.split("/")
                file_name = parts[-1]
                image_url = f"https://en.wikipedia.org/wiki/List_of_galaxies#/media/File:{file_name}"

                galaxy = columns[1].find("a").text.strip()
                constellation = columns[2].find("a").text.strip()
                origin_name = columns[3].text.strip()
                note = columns[4].text.strip()

                galaxy_data.append({
                    'Galaxy': galaxy,
                    'Constellation': constellation,
                    'Origin of Name': origin_name,
                    'Notes': note,
                    'Image URL': image_url
                })

    random.shuffle(galaxy_data)

fetch_and_shuffle_exoplanet_data()
fetch_and_shuffle_galaxy_data()

def extract_exoplanet_details(exoplanet_name):
    exoplanet_name_with_underscore = exoplanet_name.replace(" ", "_")
    url = f"http://www.exoplanetkyoto.org/exohtml/{exoplanet_name_with_underscore}.html"

    description = ""
    image_url = ""

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            description_element = soup.find("b", text=exoplanet_name)
            if description_element:
                description = description_element.find_next("li").get_text().strip()

            img_element = soup.find("img", src=True)
            if img_element:
                image_url = img_element["src"]
                image_url = image_url[1:]
                image_url = f"http://www.exoplanetkyoto.org/exohtml{image_url}"
    except Exception as e:
        return {'error': 'An error occurred while fetching planet information.'}

    exoplanet_info = {
        'exoplanet': {
            'name': exoplanet_name,
            'description': description,
            'image_url': image_url
        }
    }

    return exoplanet_info

@app.route('/exoplanets', methods=['GET'])
def get_random_exoplanet():
    if not exoplanet_data:
        return jsonify({'error': 'Exoplanet data is empty'})
    
    exoplanet_name = exoplanet_data.pop()
    exoplanet_info = extract_exoplanet_details(exoplanet_name)

    return jsonify(exoplanet_info)

@app.route('/galaxies', methods=['GET'])
def get_random_galaxy():
    if not galaxy_data:
        fetch_and_shuffle_galaxy_data()
    random_galaxy = random.choice(galaxy_data)
    return jsonify(random_galaxy)

if __name__ == '__main__':
    app.run(debug=True)
