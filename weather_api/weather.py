from configparser import ConfigParser
import argparse
from urllib import parse, request, error
import json
import sys
from pprint import pp

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

'''Fetching API from config file'''
def _get_api():
    config = ConfigParser()
    config.read('C:\\Users\\002CSC744\\Documents\\my_api\\weather_api\\secrets.ini')
    return config["openweather"]["api_key"]

def read_usr_cli_args():
    """Get input from User through CLI"""
    parser = argparse.ArgumentParser(
        description='Get weather for a CITY from CLI directly!!!'
    )

    '''Parse User input get from CLI'''
    parser.add_argument(
        "City", nargs="+", type=str, help="Enter the City Name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )

    return parser.parse_args()

def build_weather_url(city_input, imperial=False):
    api_key =_get_api()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url

def get_weather_data(query_url):
    '''Getting weather information from target URL'''
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")
    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Can't read Server response:=>>")


if __name__ == '__main__':
    user_args = read_usr_cli_args()
    #print(user_args.City, user_args.imperial)
    query_url = build_weather_url(user_args.City, user_args.imperial)
    weather_data = get_weather_data(query_url)
    #pp(weather_data)
    print(
        f"{weather_data['name']}: "
        f"{weather_data['weather'][0]['description']} "
        f"({weather_data['main']['temp']})"
    )