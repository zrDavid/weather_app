import tkinter as tk
from datetime import datetime as dt
from datetime import timezone
import requests
from PIL import Image, ImageTk

def kelvin_to_celsius(kelvin):
    return (kelvin - 273.15)

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15)*(9/5) + 32

# Creating the GUI
window = tk.Tk()
window.geometry("600x420")
window.title("Title Here")
window.configure(bg='azure')
Font_tuple = ("Segoe UI", 12, "normal")
Font_tuple_big = ("Segoe UI", 26, "bold")
defaultText = "Search for a city"
defaultCity = ""
cityName = defaultCity

def call_api(event):
    cityName = ent.get()

    GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct?"
    API_KEY = open("api_key.txt", 'r').read()
    CITY = cityName
    url = GEOCODING_URL + "q=" + CITY + "&appid=" + API_KEY

    response = requests.get(url).json()
    latitude = str(response[0]['lat'])
    longitud = str(response[0]['lon'])
    #print(f"{CITY} is at Latitude = {latitude}, Longitud = {longitud}")

    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?"
    url2 = WEATHER_URL + "lat=" + latitude + "&lon=" + longitud + "&appid=" + API_KEY
    response2 = requests.get(url2).json()
    icon_url =  "https://openweathermap.org/img/wn/10d@2x.png"
    icon_data = requests.get(icon_url)    
    
    temperature_celsius = kelvin_to_celsius(response2["main"]["temp"])
    wind_speed = response2["wind"]["speed"]
    feels_like_celsius = kelvin_to_celsius(response2["main"]["feels_like"])
    temperature_fahrenheit = kelvin_to_fahrenheit(response2["main"]["temp"])
    wind_speed = response2["wind"]["speed"]
    feels_like_fahrenheit = kelvin_to_fahrenheit(response2["main"]["feels_like"])
    humidity = response2["main"]["humidity"]

    #Deprecated way of using datetime conversion
    #sunrise_time = dt.datetime.utcfromtimestamp(response2["sys"]["sunrise"] + response2["timezone"])
    sunrise_time_ts = response2["sys"]["sunrise"] + response2["timezone"]
    sunrise_time = dt.fromtimestamp(sunrise_time_ts, tz=timezone.utc).time()
    sunset_time_ts = response2["sys"]["sunset"] + response2["timezone"]
    sunset_time = dt.fromtimestamp(sunset_time_ts, tz=timezone.utc).time()
    general_description = response2["weather"][0]["description"]

    #Getting the icon:
    icon = response2["weather"][0]["icon"]
    icon_url = (f"http://openweathermap.org/img/wn/{icon}@2x.png")
    icon_data = requests.get(icon_url)
    with open("icon.png", "wb") as f:
        f.write(icon_data.content)
    icon_image = ImageTk.PhotoImage(Image.open("icon.png"))
    
    # Fill the empty spaces:
    lblCity.config(text=cityName.title())
    lblTemp1.config(text=f"{temperature_celsius:.2f} \N{DEGREE SIGN}C")
    lblTemp2.config(text=f"({temperature_fahrenheit:.2f} \N{DEGREE SIGN}F)")
    lblCond.config(text="Weather Conditions: " + f"{general_description}")
    lblIcon.config(image=icon_image)
    lblIcon.image = icon_image
    lblHumidity.config(text=f"{humidity}" + "%")
    lblSunrise.config(text=sunrise_time)
    lblSunset.config(text=sunset_time)
    empty_entry(event)

def empty_entry(event):
    ent.delete(0, tk.END)

ent = tk.Entry(master=window, width=36, bg="white", fg="gray")
ent.grid(row=0, column=0, padx=10, pady=2, sticky='w')
ent.insert(0, defaultText)
ent.configure(font = Font_tuple)
ent.bind("<FocusIn>", empty_entry)
ent.bind("<Return>", call_api)

frm = tk.Frame(master=window, borderwidth=1, bg="azure")
frm.grid(row=1, column=0, sticky='ew')

lblCity = tk.Label(master=frm, text=cityName, width=36, height=2, bg="azure", anchor='w')
lblCity.grid(row=0, column=0, padx=10, pady=5, sticky='w', columnspan=2)
lblCity.configure(font = Font_tuple)

lblTemp1 = tk.Label(master=frm, text="\N{DEGREE SIGN}C", width=8, height=2, bg="azure", anchor='nw')
lblTemp1.grid(row=1, column=0, padx=10, pady=2, sticky='nw')
lblTemp1.configure(font = Font_tuple_big)

lblTemp2 = tk.Label(master=frm, text="\N{DEGREE SIGN}F", width=10, height=2, bg="azure", anchor='nw')
lblTemp2.grid(row=1, column=1, padx=10, pady=2, sticky='nw')
lblTemp2.configure(font = Font_tuple)

lblCond = tk.Label(master=frm, text="Weather Conditions: ", width=36, height=2, bg="azure", anchor='w')
lblCond.grid(row=2, column=0, padx=10, pady=2, sticky='w', columnspan=2)
lblCond.configure(font = Font_tuple)

lblIcon = tk.Label(master=window, text="", bg="azure")
lblIcon.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")
lblIcon.configure(font = Font_tuple)

lblHumidityFixText = tk.Label(master=window, text="Humidity: ", width=15, height=2, bg="azure", anchor='w')
lblHumidityFixText.grid(row=2, column=0, padx=10, pady=5, sticky='w')
lblHumidityFixText.configure(font = Font_tuple)

lblHumidity = tk.Label(master=window, text=" % ", width=20, height=2, bg="azure", anchor='w')
lblHumidity.grid(row=2, column=0, padx=150, pady=5, sticky='w')
lblHumidity.configure(font = Font_tuple)

lblSunriseFixText = tk.Label(master=window, text="Sunrise time: ", width=15, height=2, bg="azure", anchor='w')
lblSunriseFixText.grid(row=3, column=0, padx=10, pady=5, sticky='w')
lblSunriseFixText.configure(font = Font_tuple)

lblSunrise = tk.Label(master=window, text=" - - ", width=20, height=2, bg="azure", anchor='w')
lblSunrise.grid(row=3, column=0, padx=150, pady=5, sticky='w')
lblSunrise.configure(font = Font_tuple)

lblSunsetFixText = tk.Label(master=window, text="Sunset time: ", width=15, height=2, bg="azure", anchor='w')
lblSunsetFixText.grid(row=4, column=0, padx=10, pady=5, sticky='w')
lblSunsetFixText.configure(font = Font_tuple)

lblSunset = tk.Label(master=window, text=" - - ", width=20, height=2, bg="azure", anchor='w')
lblSunset.grid(row=4, column=0, padx=150, pady=5, sticky='w')
lblSunset.configure(font = Font_tuple)

window.mainloop()
