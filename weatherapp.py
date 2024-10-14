import tkinter as tk
from datetime import datetime as dt
from datetime import timezone
import requests

def kelvin_to_celsius(kelvin):
    return (kelvin - 273.15)

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15)*(9/5) + 32

# Creating the GUI
window = tk.Tk()
window.geometry("600x400")
window.title("Title Here")
Font_tuple = ("Segoe UI", 12, "normal")
Font_tuple_big = ("Segoe UI", 30, "bold")
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

    temperature_celsius = kelvin_to_celsius(response2["main"]["temp"])
    wind_speed = response2["wind"]["speed"]
    feels_like_celsius = kelvin_to_celsius(response2["main"]["feels_like"])
    temperature_fahrenheit = kelvin_to_fahrenheit(response2["main"]["temp"])
    wind_speed = response2["wind"]["speed"]
    feels_like_fahrenheit = kelvin_to_fahrenheit(response2["main"]["feels_like"])

    #Deprecated way of using datetime conversion
    #sunrise_time = dt.datetime.utcfromtimestamp(response2["sys"]["sunrise"] + response2["timezone"])
    sunrise_time_ts = response2["sys"]["sunrise"] + response2["timezone"]
    sunrise_time = dt.fromtimestamp(sunrise_time_ts, tz=timezone.utc).time()
    sunset_time_ts = response2["sys"]["sunset"] + response2["timezone"]
    sunset_time = dt.fromtimestamp(sunset_time_ts, tz=timezone.utc).time()
    general_description = response2["weather"][0]["description"]
    #print(f"Sunrise time happens at {sunrise_time}")

    # Fill the empty spaces:
    lblCity.config(text=cityName)
    lblTemp1.config(text=f"{temperature_celsius:.2f} \N{DEGREE SIGN}C")
    lblTemp2.config(text=f"({temperature_fahrenheit:.2f} \N{DEGREE SIGN}F)")
    lblCond.config(text=f"{general_description}")
    lblSunrise.config(text=sunrise_time)
    lblSunset.config(text=sunset_time)

    

ent = tk.Entry(master=window, width=35, bg="white", fg="gray")
ent.grid(row=0, column=0, padx=5, pady=2, sticky='w')
ent.insert(0, defaultText)
ent.configure(font = Font_tuple)
ent.bind("<Return>", call_api)

frm = tk.Frame(master=window, borderwidth=1, padx=5)
frm.grid(row=1, column=0)

lblCity = tk.Label(master=frm, text=cityName, width=36, height=2, bg="white", anchor='w')
lblCity.grid(row=0, column=0, padx=0, pady=5, sticky='w', columnspan=2)
lblCity.configure(font = Font_tuple)

lblTemp1 = tk.Label(master=frm, text="Celsius", width=8, height=2, bg="aliceblue", anchor='nw')
lblTemp1.grid(row=1, column=0, padx=0, pady=5, sticky='nw')
lblTemp1.configure(font = Font_tuple_big)

lblTemp2 = tk.Label(master=frm, text="Fahrenheit", width=10, height=2, bg="aliceblue", anchor='nw')
lblTemp2.grid(row=1, column=1, padx=0, pady=5, sticky='nw')
lblTemp2.configure(font = Font_tuple)

lblCond = tk.Label(master=frm, text="Conditions", width=36, height=2, bg="aliceblue", anchor='w')
lblCond.grid(row=2, column=0, padx=0, pady=5, sticky='w', columnspan=2)
lblCond.configure(font = Font_tuple)

lblIcon = tk.Label(master=frm, text="Conditions Icon", width=15, height=6, fg="white", bg="aliceblue")
lblIcon.grid(row=0, column=2, padx=5, pady=5, sticky="ens", rowspan=3)
lblIcon.configure(font = Font_tuple)

lblSunriseFixText = tk.Label(master=window, text="Sunrise time: ", width=15, height=2, bg="cadetblue1", anchor='w')
lblSunriseFixText.grid(row=2, column=0, padx=5, pady=5, sticky='w')
lblSunriseFixText.configure(font = Font_tuple)

lblSunrise = tk.Label(master=window, text=" - - ", width=20, height=2, bg="cadetblue1", anchor='w')
lblSunrise.grid(row=2, column=0, padx=150, pady=5, sticky='w')
lblSunrise.configure(font = Font_tuple)

lblSunsetFixText = tk.Label(master=window, text="Sunset time: ", width=15, height=2, bg="dodgerblue4", anchor='w')
lblSunsetFixText.grid(row=3, column=0, padx=5, pady=5, sticky='w')
lblSunsetFixText.configure(font = Font_tuple)

lblSunset = tk.Label(master=window, text=" - - ", width=20, height=2, bg="dodgerblue4", anchor='w')
lblSunset.grid(row=3, column=0, padx=150, pady=5, sticky='w')
lblSunset.configure(font = Font_tuple)

