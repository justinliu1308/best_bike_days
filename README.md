# best_bike_days
## Description
Fetch weather data and receive a computed output determining if there are upcoming days where the weather conditions are worth taking a few hours to go biking. This program is intended for regularly checking local weather data, so we use a set variable instead of command line user input.

There are two different applications in this repo:
1. todays_weather.py  -  Creates a simple table showing the current weather of a specified city
2. best_bike_days.py  -  Returns recommendations on upcoming days for biking based on the weather of a specified city

Daily weather requirements that would result in a recommendation are:
- Temperature between 69-79 °F
- Wind speed no more than 9 mph
- Sunny or partly sunny
- No rain in the last 24 hours

## Usage
Usage:
1. Obtain a free API key from openweathermap.org and add it to a new file "api_key.txt"
2. For both applications, set the 'city' variable at the bottom of the file to your city name and run the python file.

## Output
#![alt text](https://github.com/justinliu1308/best_bike_days/blob/main/screenshot_todays_weather.png)

## Reference
Open Weather Map website: https://openweathermap.org/
API call documentation: https://openweathermap.org/current

