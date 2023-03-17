import requests
import json
from beautifultable import BeautifulTable
#import datetime

# Fetch weather data using your unique API key from https://openweathermap.org/
API_KEY = open('api_key.txt', 'r').read()
current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
parameters = {
    'q': 'Gaithersburg',
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
    table.rows.append([timezone])
    table.columns.header = [parameters['q'] + " Weather"]
    table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Timezone"]
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    print(table)
else:
    print(f"Error fetching weather data: status code {current_weather_response.status_code}")
