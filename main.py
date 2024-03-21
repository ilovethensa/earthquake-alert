import requests
from datetime import datetime, timedelta

def fetch_earthquake_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None

def print_recent_earthquakes_in_countries(data, countries, days=1):
    if data:
        current_time = datetime.now()
        time_threshold = current_time - timedelta(days=days)
        for feature in data["features"]:
            place = feature["properties"]["place"]
            time_unix = feature["properties"]["time"] / 1000  # Convert milliseconds to seconds
            earthquake_time = datetime.utcfromtimestamp(time_unix)
            for country in countries:
                if country.lower() in place.lower() and earthquake_time >= time_threshold:
                    mag = feature["properties"]["mag"]
                    print("Magnitude:", mag)
                    print("Place:", place)
                    print("Time:", earthquake_time)
                    print("URL:", feature["properties"]["url"])
                    print()
                    requests.post("https://ntfy.sh/earthquake_alerts_lol_tht",
                        data=place,
                        headers={ "Title": f"Earthquake {mag} magnitude", "Priority": "4" })


if __name__ == "__main__":
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson"
    countries = [
        "Bulgaria",
        "Romania",
        "Serbia",
        "North Macedonia",
        "Greece",
        "Turkey",
        "Montenegro",
        "Kosovo",
        "Bosnia and Herzegovina",
        "Albania",
        "Croatia"
    ]
    earthquake_data = fetch_earthquake_data(url)
    if earthquake_data:
        print("Successfully fetched earthquake data.")
        print("Recent earthquakes in the specified countries (last day):")
        print_recent_earthquakes_in_countries(earthquake_data, countries, days=1)
    else:
        print("Failed to fetch earthquake data.")
