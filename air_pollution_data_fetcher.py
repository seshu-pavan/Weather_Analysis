import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import csv

# loading the api key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")


def unix_to_date(unix):
    """Converts unix timestamp to date in the format of DD-MM-YYYY"""
    return datetime.fromtimestamp(unix).strftime('%d-%m-%Y')


# creating a dictionary with cites as keys and their latitudes and longitudes as values
cities = \
    {
        'Ahmedabad': [23.0225, 72.5714],
        'Aizawl': [23.7271, 92.7176],
        'Amaravati': [16.5167, 80.6167],
        'Amritsar': [31.6167, 74.8500],
        'Bengaluru': [12.9699, 77.5980],
        'Bhopal': [23.2599, 77.4126],
        'Brajrajnagar': [21.8167, 83.9167],
        'Chandigarh': [30.7333, 76.7794],
        'Chennai': [13.0825, 80.2750],
        'Coimbatore': [11.0168, 76.9558],
        'Delhi': [28.7041, 77.1025],
        'Ernakulam': [9.9312, 76.2673],
        'Gurugram': [28.4595, 77.0266],
        'Guwahati': [26.1445, 91.7362],
        'Hyderabad': [17.3850, 78.4867],
        'Jaipur': [26.9124, 75.7873],
        'Jorapokhar': [23.6667, 86.3667],
        'Kochi': [9.9312, 76.2673],
        'Kolkata': [22.5726, 88.3639],
        'Lucknow': [26.8467, 80.9462],
        'Mumbai': [19.0760, 72.8777],
        'Patna': [25.5941, 85.1376],
        'Shillong': [25.5788, 91.8933],
        'Talcher': [20.9500, 85.2333],
        'Thiruvananthapuram': [8.5241, 76.9366],
        'Visakhapatnam': [17.6868, 83.2185]
    }


def get_pollution_data(city):
    """This function takes city as input and returns the pollution data of that city as key-value pairs"""
    base_url = 'http://api.openweathermap.org/data/2.5/air_pollution/history?'
    url = base_url + f'lat={cities[city][0]}&lon={cities[city][1]}&start=1606721230&end=1684999630&appid=' + API_KEY
    response = requests.get(url).json()

    # List to store unique dates
    unique_dates = []
    # List to store pollution data for each unique date
    pollution_data = []

    for item in response['list']:
        date = unix_to_date(item['dt'])
        if date not in unique_dates:
            unique_dates.append(date)
            pollution_data.append({
                'city': city,
                'date': date,
                'aqi': item['main']['aqi'],
                'co': item['components']['co'],
                'no': item['components']['no'],
                'no2': item['components']['no2'],
                'o3': item['components']['o3'],
                'so2': item['components']['so2'],
                'pm2_5': item['components']['pm2_5'],
                'pm10': item['components']['pm10'],
                'nh3': item['components']['nh3']
            })

    return pollution_data


# writing the data to a csv file
with open('Data/air_pollution_data.csv', 'w', newline='') as file:
    headers = ['city', 'date', 'aqi', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for city in cities:
        for item in get_pollution_data(city):
            writer.writerow(item)
