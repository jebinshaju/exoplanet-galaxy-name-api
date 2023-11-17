import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import random

app = Flask(__name__)

def extract_exoplanet_details(exoplanet_name):
    exoplanet_name_with_underscore = exoplanet_name.replace(" ", "_")
    url = f"http://www.exoplanetkyoto.org/exohtml/{exoplanet_name_with_underscore}.html"
    
    description = ""
    image_url = ""

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            description_element = soup.find("b", text=exoplanet_name)
            if description_element:
                description = description_element.find_next("li").get_text().strip()
                # Remove newline characters
                description = description.replace("\n", "")

            img_element = soup.find("img", src=True)
            if img_element:
                image_url = img_element["src"]
                image_url = image_url[1:]
                image_url = f"http://www.exoplanetkyoto.org/exohtml{image_url}"
    except Exception as e:
        return {'error': 'An error occurred while fetching planet information.'}

    exoplanet_info = {
        'name': exoplanet_name,
        'description': description,
        'image_url': image_url
    }

    return exoplanet_info

# def get_galaxy_details(galaxy_name):
#     url = "https://images-api.nasa.gov/search"
#     params = {
#         "q": galaxy_name,
#         "media_type": "image",
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     galaxies = []
#     for item in data["collection"]["items"]:
#         galaxy = {
#             "title": item["data"][0]["title"],
#             "description": item["data"][0]["description"],
#             "image_url": item["links"][0]["href"]
#         }
#         galaxies.append(galaxy)

#     return galaxies
@app.route('/exoplanets', methods=['GET'])
def get_random_exoplanet():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+top+300+*+from+ps+where+tran_flag=1+order+by+pl_name+asc"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    rows = soup.find_all('tr')
    exoplanets = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        exoplanet = {
            "planet_name": columns[0].text,
            "star_name": columns[2].text,
            "discovery_method": columns[6].text,
            "orbital_period": columns[7].text,
            "planet_mass": columns[22].text,
            "planet_radius": columns[23].text,
            "equilibrium_temperature": columns[24].text
        }
        exoplanet_details = extract_exoplanet_details(exoplanet["planet_name"])
        exoplanet["description"] = exoplanet_details["description"]
        exoplanet["image_url"] = exoplanet_details["image_url"]
        exoplanets.append(exoplanet)

    # Remove duplicate exoplanets
    exoplanets = [exoplanet for i, exoplanet in enumerate(exoplanets) if exoplanets.index(exoplanet) == i]

    # Return a random exoplanet
    print("higigiigig")
    return exoplanets

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
        desc = item["data"][0]["description"]
        desc = desc.replace("&amp; NASA  <b><a href=\"http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html\" rel=\"nofollow\">NASA image use policy.</a></b>  <b><a href=\"http://www.nasa.gov/centers/goddard/home/index.html\" rel=\"nofollow\">NASA Goddard Space Flight Center</a></b> enables NASA’s mission through four scientific endeavors: Earth Science, Heliophysics, Solar System Exploration, and Astrophysics. Goddard plays a leading role in NASA’s accomplishments by contributing compelling scientific knowledge to advance the Agency’s mission.  <b>Follow us on <a href=\"http://twitter.com/NASAGoddardPix\" rel=\"nofollow\">Twitter</a></b>  <b>Like us on <a href=\"http://www.facebook.com/pages/Greenbelt-MD/NASA-Goddard/395013845897?ref=tsd\" rel=\"nofollow\">Facebook</a></b>  <b>Find us on <a href=\"http://instagrid.me/nasagoddard/?vm=grid\" rel=\"nofollow\">Instagram</a></b> ","")
        galaxy = {
            "title": item["data"][0]["title"],
            "description": desc,
            "image_url": item["links"][0]["href"]
        }
        galaxies.append(galaxy)

    return galaxies

@app.route('/', methods=['GET'])
def get_random_detail():
    detail_type = random.choice(['exoplanet', 'galaxy'])

    if detail_type == 'exoplanet':
        exo = get_random_exoplanet()
        return jsonify(random.choice(exo))
    elif detail_type == 'galaxy':
        galaxies = get_galaxies()
        return jsonify(random.choice(galaxies))

if __name__ == "__main__":
    app.run(debug=True)
