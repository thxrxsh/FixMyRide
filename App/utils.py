from passlib.context import CryptContext
import requests
from config import Settings
from geopy.distance import geodesic

api_key = Settings.api_key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def calculate_road_distance(origin, destination):

    base_url = "https://maps.googleapis.com/maps/api/directions/json?"
    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "key": api_key,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if "routes" in data:
        distance = data["routes"][0]["legs"][0]["distance"]["value"]
        return distance
    return float("inf")  # Return a very large value if no route is found


def filter_by_radius(radius, origin, mechanic_coordinates):

    results = [(mechanic[0], mechanic[1]) for mechanic in mechanic_coordinates if geodesic(origin, mechanic[1]).kilometers < radius  ]
    return results