import requests
import json
import time
from beautifultable import BeautifulTable
from datetime import datetime, timedelta


def forecast(city):
    # Fetch weather data using your unique API key from https://openweathermap.org/
    API_KEY = open('api_key.txt', 'r').read()
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    parameters = {
        'q': city,
        'appid': API_KEY,
        'units': 'imperial'
    }
    response = requests.get(url, params=parameters)
    return response

def create_table(response, city):
    # Receive response and format JSON data

    response = response.json()
    # Write JSON data to file to view
    with open("json_weather.json", "w") as file:
        json.dump(response, file, indent=4)
    
    # Sort JSON into arrays by type of weather info
    local_time_raw = []
    summary_raw = []
    real_temp_raw = []
    feels_like_raw = []
    wind_raw = []
    gust_raw = []
    cloud_raw = []
    rain_raw = []
    snow_raw = []
    for i in range(len(response['list'])):
        local_time_raw.append(response['list'][i]['dt'])
        summary_raw.append(response['list'][i]['weather'][0]['description'])
        real_temp_raw.append(round(response['list'][i]['main']['temp']))
        feels_like_raw.append(response['list'][i]['main']['feels_like'])
        wind_raw.append(response['list'][i]['wind']['speed'])
        gust_raw.append(response['list'][i]['wind']['gust'])
        cloud_raw.append(response['list'][i]['clouds']['all'])
        if 'rain' in response['list'][i]:
            rain_raw.append(response['list'][i]['rain']['3h'])
        else:
            rain_raw.append(0)
        if 'snow' in response['list'][i]:
            snow_raw.append(response['list'][i]['snow']['3h']) 
        else:
            snow_raw.append(0)
    
    # Data from API is at 3-hour intervals, or 8 datapoints/day. Average the values and condence into 1 datapoint/day.
    # Get current Unix time
    current_unix_time = time.time()
    # Convert Unix time to datetime object
    current_datetime = datetime.fromtimestamp(current_unix_time)    
    unix_day_start = []
    for i in range(5):      # Free API limits data to 5-day forecast
        # Add days to datetime object
        next_day_datetime = current_datetime + timedelta(days=i+1)
        # Set time component to 00:00:00
        next_day_datetime = next_day_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        # Convert datetime object back to Unix time
        next_day_unix_time = int(next_day_datetime.timestamp())
        unix_day_start.append(next_day_unix_time)

    local_time = []
    summary = []
    real_temp = []
    feels_like = []
    wind = []
    gust = []
    cloud = []
    rain = []
    snow = []
    day = 0
    forecast_day = 0
    for i in range(len(local_time_raw)):
        if local_time_raw[i] >= unix_day_start[day]:
            pass



    # for i in range(len(summary)):
    #     print(local_time_RAW[i], summary[i])
    


    # Converting local unix time to human readable format
    # for i in range(len(local_time_RAW)):
    #     dt = datetime.fromtimestamp(local_time_RAW[i])          # Convert Unix time to datetime object
    #     date_string = dt.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime object to human-readable string
    #     local_time_RAW[i] = date_string
    #     print(date_string, summary[i])

    '''
    # Assigning weather data variables
    summary = response['weather'][0]['description']
    real_temp = str(round(response['main']['temp'])) + " °F"
    feels_like = str(round(response['main']['feels_like'])) + " °F"
    wind = str(round(response['wind']['speed'])) + " mph"
    cloud = str(response['clouds']['all']) + "% cloudy"
    # Check for rain or snow, included in JSON only if present in current weather conditions
    rain = 0
    if 'rain' in response:
        rain = str(response['rain']['1h']) + " in"
    snow = 0
    if 'snow' in response:
        snow = str(response['snow']['1h']) + " in"
    timezone = round(response['timezone'] / 3600)
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
    '''

    # Results shown up until current time of the 5th day from today due to limits on free API version
    # If you are running the application at 11am on Monday, it will only receive data until 11am Saturday
    # and thus the output for Saturday will be based on only the data received.

city = 'District of Columbia'
#city = 'taipei'
#city = 'atlanta'
response = forecast(city)
if response.status_code == 200:
    create_table(response, city)
else:
    print(f"Error fetching weather data: status code {response.status_code}")



