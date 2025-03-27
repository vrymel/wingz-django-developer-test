import random
import requests
import datetime

"""
curl --location 'http://localhost:8000/api/rides/' \
--header 'Authorization: Token 94cdd6809c5237b38c6320eb4902e7d7473ed9b5' \
--header 'Content-Type: application/json' \
--data '{
    "id_rider": 1,
    "id_driver": 2,
    "status": "new",
    "pickup_latitude": "14.5998083",
    "pickup_longitude": "120.9628558",
    "dropoff_latitude": "14.5998083",
    "dropoff_longitude": "120.9628558",
    "pickup_time": "2025-05-22 08:00:00"
}'
"""

latitude = (14.4396129, 14.8411207)
longitude = (120.944883,121.2428874)

def get_random_coordinates():
    random_latitude = round(random.uniform(latitude[0], latitude[1]), 7)
    random_longitude = round(random.uniform(longitude[0], longitude[1]), 7)
    
    return random_latitude, random_longitude


for i in range(900000):
    pickup_latitude, pickup_longitude = get_random_coordinates()
    dropoff_latitude, dropoff_longitude = get_random_coordinates()

    url = 'http://localhost:8000/api/rides/'
    headers = {
        'Authorization': 'Token 94cdd6809c5237b38c6320eb4902e7d7473ed9b5',
        'Content-Type': 'application/json'
    }
    data = {
        "id_rider": 1,
        "id_driver": 2,
        "status": "new",
        "pickup_latitude": f"{pickup_latitude}",
        "pickup_longitude": f"{pickup_longitude}",
        "dropoff_latitude": f"{dropoff_latitude}",
        "dropoff_longitude": f"{dropoff_longitude}",
        "pickup_time": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Response {i+1}: {response.status_code}, {response.text}")