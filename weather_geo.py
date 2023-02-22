import requests

API_KEY = "07abb8b98b7be8514d9aa2f35047dff8"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_GEO = "http://api.openweathermap.org/geo/1.0/direct"

city = input("Dawaj miasto: ")
request_url_geo = f"{BASE_URL_GEO}?q={city}&limit=1&appid={API_KEY}"
response_geo = requests.get(request_url_geo)

if response_geo.status_code == 200:
    data_geo = response_geo.json()
    lat = data_geo[0]['lat']
    lon = data_geo[0]['lon']
else:
    print("ERROR")

request_url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}"
response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    print(f"Pogoda: {weather}")
    print(f"Temperatura: {round(temp - 273.15, 2)}")
else:
    print("ERROR")
