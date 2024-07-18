import sys
import json
import requests
import textwrap
import datetime
import configparser
from pathlib import Path

location = "Seattle"

config = configparser.ConfigParser()
config.read(Path(__file__).with_name('settings.cfg'))
appId = config.get('KEYS','appId')

url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={appId}'

httpResponse = requests.get(url)

print(json.dumps(httpResponse.json(), indent=3))

if httpResponse.status_code == 200:
    data = httpResponse.json()
    if len(data):
        coordinates = dict()
        coordinates['lat'] = data[0]['lat']
        coordinates['lon'] = data[0]['lon']
    else:
        sys.exit(f"Location not found for {location}")
else:
    sys.exit(f"{httpResponse.status_code} {httpResponse.reason}")

latitude = str(coordinates['lat'])

longitude = str(coordinates['lon'])

count = 8

forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?units=imperial&cnt={count}&lat={latitude}&lon={longitude}&appid={appId}'

forecastHttpResponse = requests.get(forecast_url)

if forecastHttpResponse.status_code != 200:
    sys.exit(f'{forecastHttpResponse.status_code}')

print(json.dumps(forecastHttpResponse.json(), indent=3))

# print the forecast (a bare print() function is called first to make a clean line in the output)
print()
print(f'{3 * count}-hour forecast for {httpResponse.json()["city"]["name"]} (3-hour increments):')

for x in forecastHttpResponse.json()["list"]:
    print(textwrap.dedent(f'''
        {datetime.datetime.fromtimestamp(x["dt"]).strftime("%a, %b %-d, %Y, %-I:%M %p")}
        Conditions: {"/".join(list(map(lambda x: x["main"], x["weather"])))}
        Temp: {round(x["main"]["temp"])}°F
        Feels like: {round(x["main"]["feels_like"])}°F
        Low temp: {round(x["main"]["temp_min"])}°F
        High temp: {round(x["main"]["temp_max"])}°F
        Humidity: {round(x["main"]["humidity"])}%
    '''))