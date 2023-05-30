import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# loading the api key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")


class UnitsConverter:
    """Converts the weather measurements into human readable format"""

    def kelvin_to_celsius(self, kelvin):
        """Converts kelvin to celsius"""
        return kelvin - 273.15

    def unix_to_date(self, unix):
        """Converts unix timestamp to date in the format of DD-MM-YYYY"""
        return datetime.fromtimestamp(unix).strftime('%d-%m-%Y')

    def unix_to_time(self, unix):
        """Converts unix timestamp to time in the format of HH:MM"""
        return datetime.fromtimestamp(unix).strftime('%H:%M')

    def speed_to_kmph(self, speed):
        """Converts speed from m/s to km/h"""
        return speed * 3.6


units_converter = UnitsConverter()


def get_weather_data(city):
    """This function takes city as input and returns the weather data of that city as key value pairs"""
    base_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?'
    url = base_url + f'q={city}&cnt=1&appid=' + API_KEY
    response = requests.get(url).json()
    return {
        'city': city,
        'date': units_converter.unix_to_date(response['list'][0]['dt']),
        'sunrise': units_converter.unix_to_time(response['list'][0]['sunrise']),
        'sunset': units_converter.unix_to_time(response['list'][0]['sunset']),
        'temp_day': round(units_converter.kelvin_to_celsius(response['list'][0]['temp']['day']), 2),
        'temp_night': round(units_converter.kelvin_to_celsius(response['list'][0]['temp']['night']), 2),
        'feels_like_day': round(units_converter.kelvin_to_celsius(response['list'][0]['feels_like']['day']), 2),
        'pressure': round(response['list'][0]['pressure'], 2),
        'humidity': round(response['list'][0]['humidity'], 2),
        'weather_condition': response['list'][0]['weather'][0]['main'],
        'speed': round(response['list'][0]['speed'], 2)
    }


# creating a list of cities to get weather data
cities = ['Vishakhapatnam', 'Hyderabad', 'Delhi', 'Mumbai', 'Chennai', 'Bengaluru', 'Kolkata',
          'Jaipur', 'Shimla', 'Kochi', 'Ahmedabad', 'Guwahati']

for city in cities:
    print(get_weather_data(city))
