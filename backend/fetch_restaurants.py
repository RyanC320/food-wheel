import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def fetch_from_openstreetmap(lat, lon):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": "restaurant",
        "format": "json",
        "limit": 30,
        "lat": lat,
        "lon": lon,
        "bounded": 1,
        "viewbox": f"{lon-0.02},{lat+0.02},{lon+0.02},{lat-0.02}"
    }
    headers = {
        "User-Agent": "FoodWheelStudentProject/1.0"
    }
    response = requests.get(url, params=params, headers=headers)
    print("STATUS CODE:", response.status_code)
    data = response.json()

    restaurants = []
    for place in data:
        name = place.get("display_name", "").split(",")[0]
        lat_val = place.get("lat")
        lon_val = place.get("lon")
        if name:
            restaurants.append((name, None, lat_val, lon_val))

    return restaurants

def save_to_database(restaurants):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear out old test data first
    cursor.execute("DELETE FROM restaurants_cache")

    # Insert the real data
    insert_query = """
        INSERT INTO restaurants_cache (name, cuisine, latitude, longitude)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(insert_query, restaurants)
    conn.commit()

    print(f"Inserted {cursor.rowcount} restaurants into the database.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Orlando coordinates - change these to your actual area if you want
    lat = 28.5383
    lon = -81.3792

    print("Fetching restaurants from OpenStreetMap...")
    restaurants = fetch_from_openstreetmap(lat, lon)
    print(f"Found {len(restaurants)} restaurants.")

    print("Saving to database...")
    save_to_database(restaurants)

    print("Done!")