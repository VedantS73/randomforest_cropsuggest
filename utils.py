from datetime import date
import requests
from bs4 import BeautifulSoup
import re
from flask import jsonify

def getweather():
    weather = {}
    url = "https://weather.com/en-IN/weather/today/l/4daa523297672007c289f6ae03c3eb4ea9c6e041d577e3c2bb3e6e8abcf33a4c"
    day = date.today().day
    weather['Day'] = day
    month = date.today().month
    weather['Month'] = month
    year = date.today().year
    weather['Year'] = year

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    weather['Time'] = soup.find("div", class_="CurrentConditions--header--kbXKR").text[-9:]
    weather['Temperature'] = soup.find("span", class_="CurrentConditions--tempValue--MHmYY").text[:-1]
    weather['Condition'] = soup.find("div", class_="CurrentConditions--phraseValue--mZC_p").text

    highlow = soup.find("div", class_="WeatherDetailsListItem--wxData--kK35q").text
    weather['High'] = highlow.split("/")[0][:-1] if highlow.split("/")[0][:-1].isdigit() else 0
    weather['Low'] = highlow.split("/")[1][1:-1] if highlow.split("/")[1][1:-1].isdigit() else 0

    weather['Wind'] = ''.join(char for char in soup.select("div.WeatherDetailsListItem--wxData--kK35q")[1].text[5:-4] if char.isdigit())
    weather['Humidity'] = soup.select("div.WeatherDetailsListItem--wxData--kK35q")[2].text[:-1]
    weather['Dew Point'] = soup.select("div.WeatherDetailsListItem--wxData--kK35q")[3].text[:-1]

    pressure = soup.select("div.WeatherDetailsListItem--wxData--kK35q")[4].text
    match = re.search(r'\d+(\.\d+)?', pressure)
    weather['Pressure'] = float(match.group()) if match else None

    weather['Visibility'] = soup.select("div.WeatherDetailsListItem--wxData--kK35q")[6].text[:-3]
    weather['Heat'] = "YES" if int(weather['Temperature']) >= 30 else "NO"
    weather['Wet'] = "YES" if int(weather['Humidity']) >= 80 else "NO"

    return jsonify(weather)

def get_weather_by_lat_lon(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=acad760cf034c5dc786a0eb8a03957f3'
    response = requests.get(url)
    data = response.json()
    weather_data = {
        'Condition': data['weather'][0]['description'],
        'Temperature': data['main']['temp'],
        'Humidity': data['main']['humidity'],
        'Wind Speed': data['wind']['speed'],
        # Add more weather parameters as needed
    }
    return jsonify(weather_data)

def get_weather_by_polygon(points):
    first_pt = points[0]
    lat, lon = first_pt['lat'], first_pt['lon']
    return get_weather_by_lat_lon(lat, lon)

def get_7_day_forecast(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=7&appid=acad760cf034c5dc786a0eb8a03957f3'
    response = requests.get(url)
    data = response.json()
    return data
