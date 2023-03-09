import requests

# Using OpenWeatherMap for weather API
# Replace YOUR_API_KEY with your actual API key from OpenWeatherMap
API_KEY = 'YOUR_API_KEY'

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        return f"The temperature in {city} is {temperature}°C, the humidity is {humidity}%, and the weather is {description}."
    else:
        print("Error fetching weather data")
        return "Sorry, we couldn't get the weather information for that city."

# Example usage: get the weather for New York City
print(get_weather('New York'))