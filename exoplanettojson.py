import json
import requests
from bs4 import BeautifulSoup

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

    return exoplanets

exoplanets_data = get_random_exoplanet()

# Write exoplanets data to a JSON file
with open('exoplanets.json', 'w') as f:
    json.dump(exoplanets_data, f)
