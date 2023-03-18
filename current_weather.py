import requests
import json
from beautifultable import BeautifulTable


def get_weather(city):
    # Fetch weather data using your unique API key from https://openweathermap.org/

    API_KEY = open('api_key.txt', 'r').read()
    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {
        'q': city,
        'appid': API_KEY,
        'units': 'imperial'
    }
    current_weather_response = requests.get(current_weather_url, params=parameters)
    return current_weather_response

def create_table(current_weather_response, city):
    # Receive response and format JSON data

    current_weather_response = current_weather_response.json()
    # Write JSON data to file to view
    with open("current_weather_response.json", "w") as file:
        json.dump(current_weather_response, file, indent=4)
    # Assigning weather data variables
    summary = current_weather_response['weather'][0]['description']
    real_temp = str(round(current_weather_response['main']['temp'])) + " °F"
    feels_like = str(round(current_weather_response['main']['feels_like'])) + " °F"
    wind = str(round(current_weather_response['wind']['speed'])) + " mph"
    cloud = str(current_weather_response['clouds']['all']) + "% cloudy"
    # Check for rain or snow, included in JSON only if present in current weather conditions
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
    table = BeautifulTable()
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
    table.columns.header = [city + " Weather"]
    if rain and snow:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Rain", "Snow", "Timezone"]
    elif rain:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Rain", "Timezone"]
    elif snow:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Snow", "Timezone"]
    else:
        table.rows.header = ["Summary", "Real Temp", "Feels Like", "Wind", "Cloudiness", "Timezone"]
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    print(table)


city = 'District of Columbia'
response = get_weather(city)
if response.status_code == 200:
    create_table(response, city)
else:
    print(f"Error fetching weather data: Status code {response.status_code}")


# Additional testing for different regions to check rain, snow, timezone rows
'''
cities = ['Miami', 'Denver', 'Los Angeles', 'Seattle', 'Anchorage', 'Beijing', 'Moscow', 'Mexico City', 'Tahiti', 'Munich']
for city in cities:
    response = get_weather(city)
    if response.status_code == 200:
        create_table(response, city)
    else:
        print(f"Error fetching weather data: status code {response.status_code}")
'''
