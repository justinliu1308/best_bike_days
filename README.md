# best_bike_days
## Description
Fetches weather data and displays current weather on the command line, current weather in an external window, and computes a response determining if there are upcoming days where the weather conditions are worth taking a few hours off to go biking.

There are three applications in this repo:
1. current_weather_v2.py - Opens an external window where the user can search for current weather via GUI.
2. current_weather.py  -  Creates a simple, organized table via command line showing the current weather of a specified city.
3. best_bike_days.py  -  Returns command line table of recommendations for biking days based on the 16-day weather forecast of a specified city.

Daily weather requirements that would result in a recommendation for biking are:
- Temperature between 55-85 °F
- Wind speed no more than 15 mph
- No preciptation forecasted for the day, and less than 0.2 inches of precipitation in the previous 24 hours
- The recommendation also considers wind gusts and the apparent temperature / real feel

## Usage
1. Obtain a free API key from https://openweathermap.org/ and add it to a new file "api_key.txt". This is necessary for all the applications.
2. For the GUI (current_weather_v2.py), just run the file. 
3. For the command line interface applications (current_weather.py and best_bike_days.py), set the 'city' variable at the bottom of the file to your city name and run the python file. The string can just be '{city}', or it can be '{city},{state},{country}'. For example: 'Arlington' or 'Arlington,VA,US'. By just using the city, openweathermap may return the wrong weather data since not all city names are unique. Therefore, it is recommended to use city, state, and country.

## Weather API details
- In both versions of current_weather.py, data is fetched from https://openweathermap.org/ for the current day.
- In best_bike_days.py, the specified city is geocoded through the geocoding API from https://openweathermap.org/, and the returned coordinates are used to fetch the 16-day weather forecast from https://open-meteo.com/.
- Originally, openweathermap was considered for a multi-day forecast, but their free API only provides multi-day forecast in the form of 5 day / 3 hour forecast data (an exessive 40 sets of data limited to only 5 days). The 16 day forecast, which is more suitable, requires a paid subscription - so instead, open-meteo is used as it provides a 16-day forecast free of charge.

## Output
Current weather version 2:

![alt text](https://github.com/justinliu1308/best_bike_days/blob/main/screenshots/weather_gui_tool_rain.png)

Current weather:

![alt text](https://github.com/justinliu1308/best_bike_days/blob/main/screenshots/current_weather_screenshot.png)

Best bike days recommendations:

![alt text](https://github.com/justinliu1308/best_bike_days/blob/main/screenshots/best_bike_days_screenshot.png)

## Reference
Open Weather Map website: https://openweathermap.org/

Current weather API call docs: https://openweathermap.org/current/

Geocoding API call docs: https://openweathermap.org/api/geocoding-api/

Open-Meteo weather API call docs: https://open-meteo.com/en/docs/


