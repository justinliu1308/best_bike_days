from tkinter import *       # need to import tinker as a whole first
import tkinter as tk        # then import tkinter as tk
import tkinter.messagebox
import requests
from PIL import ImageTk, Image


def get_weather():
    city = entry.get()
    API_KEY = open('api_key.txt', 'r').read()
    url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {
        'q':city,
        'appid':API_KEY,
        'units':'imperial'
    }
    response = requests.get(url, params=parameters)
    response = response.json()
    try:
        temperature = str(round(response['main']['temp'])) + " °F"
        wind = str(round(response['wind']['speed'])) + " mph"
        cloud = str(response['clouds']['all']) + "% cloudy"

        location_.configure(text=city + " Weather")
        temperature_.configure(text=temperature)
        wind_.configure(text=wind)
        cloud_.configure(text=cloud)
    except:
        pass


root = Tk()
root.title("Weather Forecast - Best Bike Days")
root.configure(bg="#1C9CF6")
root.geometry("450x750")        # dimensions in width x height

title = Label(root, text="What's the weather?", width=40, font=("Calibri 30 bold"), bg="#1C9CF6", fg="white")
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
tk.Button(root, text="Search", width=10, command=get_weather).pack(pady=7)

location_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
temperature_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
wind_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
cloud_ = Label(root , font=("Calibri 18"), bg="#1C9CF6", fg="white")
location_.pack()
temperature_.pack()
wind_.pack()
cloud_.pack()

root.mainloop()