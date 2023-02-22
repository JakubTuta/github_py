import requests

API_KEY = "07abb8b98b7be8514d9aa2f35047dff8"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = input("Dawaj miasto: ")
request_url = f"{BASE_URL}?q={city}&appid={API_KEY}"
response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    print(f"Pogoda: {weather}")
    print(f"Temperatura: {round(temp - 273.15, 2)}")
else:
    print("ERROR")
