import requests
import json
from beautifultable import BeautifulTable


def main():
    def get_geocode(city_state_country):
        # Geocode the target city with openweathermap API: https://openweathermap.org/api/geocoding-api
        API_KEY = open('api_key.txt', 'r').read()
        geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
        geocode_parameters = {
            'q':city_state_country,  # {city name},{state code},{country code} - last two optional. 'Rockville,MD,US'
            'appid':API_KEY,
            'limit':5
        }
        geocode_response = requests.get(geocode_url, params=geocode_parameters)
        if geocode_response.status_code != 200:
            print(f"Error getting geocode response from openweathermap.org: Status code {geocode_response.status_code}")
            return False, False
        geocode_response = geocode_response.json()
        with open("geocode.json", "w") as file:
            json.dump(geocode_response, file, indent=4)
        lat = geocode_response[0]['lat']
        long = geocode_response[0]['lon']
        return lat, long

    def get_forecast(lat, long):
        # Use geocode to get weather data from https://open-meteo.com/en/docs (free to use and no API key required)
        # Provides daily forecast for 16 days
        url = 'https://api.open-meteo.com/v1/forecast'
        daily_parameters = (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "apparent_temperature_max,"
            "apparent_temperature_min,"
            "precipitation_sum,"
            "weathercode,"
            "windspeed_10m_max,"
            "windgusts_10m_max"
        )
        parameters = {
            'latitude':lat,
            'longitude':long,
            'daily': daily_parameters,
            'current_weather':True,
            'temperature_unit':'fahrenheit',
            'windspeed_unit':'mph',
            'precipiation_unit':'inch',
            'timezone':'auto',
            'past_days':1,
            'forecast_days':16,
        }
        response = requests.get(url, params=parameters)
        if response.status_code != 200:
            print(f"Error fetching weather data: Status code {response.status_code}")
            return False
        response = response.json()
        with open("best_bike_days_response.json", "w") as file:
            json.dump(response, file, indent=4)
        return response

    def find_best_bike_days(response, city):
        day = []
        real_max_temp = []
        apparent_max_temp = []
        precipitation = []
        weathercode = []
        wind_max = []
        gusts_max = []
        for i in range(len(response['daily']['time'])):
            day.append(response['daily']['time'][i])
            real_max_temp.append(response['daily']['temperature_2m_max'][i])
            apparent_max_temp.append(response['daily']['apparent_temperature_max'][i])
            precipitation.append(response['daily']['precipitation_sum'][i])
            weathercode.append(response['daily']['weathercode'][i])
            wind_max.append(response['daily']['windspeed_10m_max'][i])
            gusts_max.append(response['daily']['windgusts_10m_max'][i])
        # print(real_max_temp)
        # print(apparent_max_temp)
        # print(precipitation)
        # print(weathercode)
        # print(wind_max)
        # print(gusts_max)

        # Weathercode description key
        weathercode_key = {
            0:'Clear sky',
            1:'Mainly clear',
            2:'Partly cloudy',
            3:'Overcast',
            45:'Fog',
            48:'Depositing rime fog',
            51:'Light drizzle',
            53:'Moderate drizzle',
            55:'Intense drizzle'
            # Codes 56 and above indicate unsuitable conditions; omitted from weathercode_key
        }
        # Analyzing data starting from index 1; index 0 is yesterday's weather history
        recommend_index = []
        for i in range(1, len(real_max_temp)):
            if real_max_temp[i] < 55 or real_max_temp[i] > 85:
                continue
            elif apparent_max_temp[i] < 50 or apparent_max_temp[i] > 85:
                continue
            elif precipitation[i] > 0 or precipitation[i-1] > 0.2:
                continue
            if weathercode[i] > 55:
                continue
            elif wind_max[i] > 15:
                continue
            elif gusts_max[i] > 35:
                continue
            else:
                recommend_index.append(i)
        # Format days to remove excess content (year and prefix zeroes in days, months). Default: 2023-03-16
        for d in recommend_index:
            date_month = day[d][5:7]
            date_day = day[d][8:]
            if date_month[0] == '0':
                date_month = date_month[1]
            if date_day[0] == '0':
                date_day = date_day[1]
            day[d] = date_month + '/' + date_day
        # Create table
        if len(recommend_index) > 0:
            table = BeautifulTable()
            table.rows.append(['Max Temp', 'Apparent Max', 'Max Wind', 'Description'])
            for d in recommend_index:
                table.rows.append([str(round(real_max_temp[d])) + ' °F', str(round(apparent_max_temp[d])) + ' °F', str(round(wind_max[d])) + ' mph', weathercode_key[weathercode[d]]])
            table.columns.header = ['', city, 'Weather', '']
            table.rows.header = [''] + [day[d] for d in recommend_index]
            table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
            print(table)
        else:
            print("Unfortunately, no upcoming days are recommended for biking in the current 16-day forecast.")

    city = 'Rockville,MD,US'
    lat, long = get_geocode(city)
    if lat == False:
        return
    response = get_forecast(lat, long)
    if response == False:
        return
    find_best_bike_days(response, city.split(',')[0])

if __name__ == "__main__":
    main()
