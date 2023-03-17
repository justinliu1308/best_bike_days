import requests
import json
from beautifultable import BeautifulTable

# Fetch weather data using your unique API key from https://openweathermap.org/
API_KEY = open('api_key.txt', 'r').read()
current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
parameters = {
    'q': 'Seattle',
    'appid': API_KEY,
    'units': 'imperial'
}
current_weather_response = requests.get(current_weather_url, params=parameters)
# Receive and format response
if current_weather_response.status_code == 200:
    current_weather_response = current_weather_response.json()
    # Write JSON data to file to view
    with open("json_weather.json", "w") as file:
        json.dump(current_weather_response, file, indent=4)
    # Assigning weather data variables
    table = BeautifulTable()
    summary = current_weather_response['weather'][0]['description']
    real_temp = str(round(current_weather_response['main']['temp'])) + " °F"
    feels_like = str(round(current_weather_response['main']['feels_like'])) + " °F"
    wind = str(round(current_weather_response['wind']['speed'])) + " mph"
    cloud = str(current_weather_response['clouds']['all']) + "% cloudy"
    rain = 0
    if 'rain' in current_weather_response:
        rain = str(current_weather_response['rain']['1h']) + " in"
    snow = 0
    if 'snow' in current_weather_response:
        snow = str(current_weather_response['snow']['1h']) + " in"
    timezone = round(current_weather_response['timezone'] / 3600)
    if timezone >= 0:
        timezone = "UTC+" + str(timezone)
    else:
        timezone = "UTC" + str(timezone)
    # Creating table
    table.rows.append([summary])
    table.rows.append([real_temp])
    table.rows.append([feels_like])
    table.rows.append([wind])
    table.rows.append([cloud])
    if rain:
        table.rows.append([rain])
    if snow:
        table.rows.append([snow])
    table.rows.append([timezone])
    table.columns.header = [parameters['q'] + " Weather"]
    if rain and snow:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Rainfall", "Snowfall", "Timezone"]
    elif rain:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Rainfall", "Timezone"]
    elif snow:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Snowfall", "Timezone"]
    else:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Timezone"]
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    print(table)
else:
    print(f"Error fetching weather data: status code {current_weather_response.status_code}")


# forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
# forecast_response = requests.get(forecast_url, params=parameters)
# print(forecast_response.url)

#     weather_data = response.json()
#     temperature = weather_data['main']['temp']
#     humidity = weather_data['main']['humidity']
#     description = weather_data['weather'][0]['description']
#     return f"The temperature in {city} is {temperature}°C, the humidity is {humidity}%, and the weather is {description}."
