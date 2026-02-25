import requests

def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    return data["current_weather"]

# Apply a penalty based on temperature and windspeed
def weather_penalty(weather):
    temp = weather.get("temperature")
    windspeed = weather.get("windspeed")
    system_penalty = 0

    if temp is None:
        system_penalty += 0.2

    if windspeed and windspeed > 30:
        system_penalty += 0.1


    # print(f"This is the applied penalty: {system_penalty}")
    return system_penalty