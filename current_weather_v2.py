from tkinter import *       # import tinker as a whole first
import tkinter as tk        # then import tkinter as tk
import tkinter.messagebox
import requests
import datetime
from PIL import ImageTk, Image


def get_date():
    # Get current date and format for display

    curr_date = datetime.datetime.now()
    date_f = curr_date.strftime("%A, %m/%d/%Y") # date formatted like 'Sunday, 03/19/2023'
    date_f_items = date_f.split(',')
    weekday, date = date_f_items[0], date_f_items[1].strip()
    date_nums = date.split('/')
    if date_nums[0][0] == '0':
        date_nums[0] = date_nums[0][1]
    if date_nums[1][0] == '0':
        date_nums[1] = date_nums[1][1]
    date = '/'.join(date_nums)
    display_date = weekday + ', ' + date
    return display_date

def get_weather():
    # Fetch weather data using your unique API key from https://openweathermap.org/

    city = entry.get()
    search_history.append(city)
    API_KEY = open('api_key.txt', 'r').read()
    url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {
        'q':city,
        'appid':API_KEY,
        'units':'imperial'
    }
    response = requests.get(url, params=parameters)
    status_code = response.status_code
    response = response.json()
    try:
        # Store weather details from API
        summary = "Description:   " + response['weather'][0]['description'].title()
        real_temp = "Temperature:   " + str(round(response['main']['temp'])) + " °F"
        feels_like = "Real Feel:   " + str(round(response['main']['feels_like'])) + " °F"
        wind = "Wind:   " + str(round(response['wind']['speed'])) + " mph"
        cloud = "Cloudiness:   " + str(response['clouds']['all']) + "% cloudy"

        # Check for rain or snow (included in JSON only if present in current weather conditions)
        rain = 0
        snow = 0
        if 'rain' in response:
            rain = "Rain:   " + str(response['rain']['1h']) + " in"
        else:
            rain = ''
        rain_.configure(text=rain)
        if 'snow' in response:
            snow = "Snow:   " + str(response['snow']['1h']) + " in"
        else:
            snow = ''
        snow_.configure(text=snow)
        timezone = round(response['timezone'] / 3600)
        if timezone >= 0:
            timezone = "Timezone:   " + "UTC+" + str(timezone)
        else:
            timezone = "Timezone:   " + "UTC" + str(timezone)

        # Format city name for display and retrieve date
        city = city.title()
        display_city = city.split(',')[0]
        display_date = get_date()

        # Configure the rest of the widgets
        heading_.configure(text=display_city + " Weather")
        date_.configure(text=display_date)
        summary_.configure(text=summary)
        real_temp_.configure(text=real_temp)
        feels_like_.configure(text=feels_like)
        wind_.configure(text=wind)
        cloud_.configure(text=cloud)
        timezone_.configure(text=timezone)
    except:
        tkinter.messagebox.showinfo("Error",f"Error fetching weather data: City not found.\nStatus code {status_code}.")

def show_info():
    message_info = "Last updated March 19, 2023.\nMade by Justin Liu."
    tkinter.messagebox.showinfo(title="Info", message=message_info)

def check_history():
    if len(search_history) == 0:
        history_info = "There is no history to show."
    else:
        while len(search_history) > 15:
            search_history.pop(0)
        location_string = ''
        for item in reversed(search_history):
            location_string += "\n" + item
        history_info = "Showing last 15 location searches:\n" + location_string
    tkinter.messagebox.showinfo(title="Search History", message=history_info)

# Create tkinter window
root = Tk()

# Create menu / tool bar
menubar = Menu(root)

history_menu = Menu(menubar, tearoff=0)
history_menu.add_command(label="Show History", command=check_history)
menubar.add_cascade(label="Search History", menu=history_menu)
search_history = []

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_info)
help_menu.add_separator()
help_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Help", menu=help_menu)

# Configure the window
root.configure(menu=menubar, bg="#1C9CF6")
root.title("Weather Tool - Current Weather")
root.geometry("600x720")        # window dimensions in width x height

# Add widgets - pack() automatically positions widgets without needing specific coordinates
title = Label(root, text="What's the current weather?", width=40, font=("Calibri 30 bold"), bg="#1C9CF6", fg="white")
title.pack(pady=3)

canvas = Canvas(root, width=240, height=135)
canvas.pack()
img = Image.open("weather_icon.png")
img = img.resize((245, 140))
weather_img = ImageTk.PhotoImage(img)                   # convert the image to a format tkinter can display
canvas.create_image(0,0, anchor=NW, image=weather_img)  # add image to the canvas

label = Label(root, text="Enter your city:", font=("Calibri 20"), bg="#1C9CF6", fg="white")
label.pack(pady=4)
entry = Entry(root, width=50)
entry.pack()
sample = Label(root, text='Example: "Alexandria" or "Alexandria,VA,US"', font=("Calibri 10"), bg="#1C9CF6", fg="white")
sample.pack()
search = tk.Button(root, text="Search", width=10, command=get_weather)
search.pack(pady=7)
root.bind("<Return>", lambda event: search.invoke())

heading_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
heading_.pack()
date_ = Label(root , font=("Calibri 10"), bg="#1C9CF6", fg="white")
date_.pack()
summary_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
summary_.pack()
real_temp_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
real_temp_.pack()
feels_like_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
feels_like_.pack()
wind_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
wind_.pack()
cloud_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
cloud_.pack()
rain_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
rain_.pack()
snow_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
snow_.pack()
timezone_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
timezone_.pack()

root.mainloop()
