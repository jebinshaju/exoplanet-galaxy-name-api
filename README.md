


# Exoplanet Galaxy Name API

The Exoplanet Galaxy Name API is a Flask-based API designed to provide random details about exoplanets and galaxies. Exoplanet information is scraped from [Exoplanet Kyoto](http://www.exoplanetkyoto.org/), while galaxy information is sourced from NASA's [Images API](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf).

## Overview

This API offers a simple way to retrieve random details about exoplanets and galaxies. The information is fetched from reputable sources and stored in JSON files for efficient retrieval.

## Usage

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jebinshaju/exoplanet-galaxy-name-api.git
   cd exoplanet-galaxy-name-api
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API:**

   ```bash
   python app.py
   ```

   The API will be running on `http://127.0.0.1:5000/`.

### Endpoints

#### `/shuffle`
#### `https://apiexoplanet.azurewebsites.net/shuffle`

- **Method:** `GET`
- **Description:** Returns a random item from either the exoplanets or galaxies list.
- **Details:**
  - Items are not repeated in the first 20 requests.
  - The API internally maintains a list of recently returned items to ensure uniqueness.

## Project Structure

- **`app.py`**: Flask application defining API endpoints.
- **`exoplanettojson.py`**: Script to fetch and save exoplanet data to `exoplanets.json`.
- **`galaxiestojson.py`**: Script to fetch and save galaxy data to `galaxies_data.json`.
- **`exoplanets.json`**: JSON file containing exoplanet details.
- **`galaxies_data.json`**: JSON file containing galaxy details.

## How the API Works

1. Upon starting the Flask application (`app.py`), it loads pre-existing exoplanet and galaxy data from the respective JSON files (`exoplanets.json` and `galaxies_data.json`).

2. The `/shuffle` endpoint is designed to provide a random item, ensuring that the same item is not repeated in the first 20 requests. This is achieved by maintaining a deque (`recent_items`) that stores the recently returned items.

3. When a request is made to `/shuffle`, the API randomly selects whether to provide exoplanet or galaxy details, retrieves a random item from the chosen category, checks if it's in the recent items list, and repeats the process until a unique item is found.

## Acknowledgments

- Exoplanet data: [Exoplanet Kyoto](http://www.exoplanetkyoto.org/)
- Galaxy data: NASA's [Images API](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
