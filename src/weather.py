import requests

WEATHER_API_KEY = 'a420cab78ccaeb4f0c39e6f9b952c05d'


def get_weather(city: str):
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        uv_index = get_uv_index(lat, lon)
        return weather_data['weather'][0]['description'], weather_data['main']['temp'], uv_index
    else:
        return None


def get_uv_index(lat, lon):
    uv_url = f'http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    uv_response = requests.get(uv_url)
    if uv_response.status_code == 200:
        uv_data = uv_response.json()
        return uv_data['value']
    else:
        return None

