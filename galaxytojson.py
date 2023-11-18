import requests
import json

def get_galaxies():
    url = "https://images-api.nasa.gov/search"
    params = {
        "q": "galaxy",
        "media_type": "image",
        "page_size": 300,
    }

    response = requests.get(url, params=params)
    data = response.json()

    galaxies = []
    for item in data["collection"]["items"]:
        # Extract image URL with a .jpg extension
        image_url = next((link["href"] for link in item["links"] if link["href"].lower().endswith(('.jpg', '.jpeg'))), None)

        galaxy = {
            "title": item["data"][0]["title"],
            "nasa_id": item["data"][0]["nasa_id"],
            "date_created": item["data"][0]["date_created"],
            "short_description": item["data"][0].get("description_508", ""),
            "description": item["data"][0]["description"],
            "image_url": image_url,
        }
        galaxies.append(galaxy)

    return galaxies

if __name__ == "__main__":
    galaxies_data = get_galaxies()

    # Write the details to a JSON file with a heading
    json_data = {"galaxies": galaxies_data}
    with open('galaxies_data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
