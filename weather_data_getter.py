import os
import pandas as pd
from dotenv import load_dotenv

from geopy.geocoders import Nominatim
import PySAM.ResourceTools as rT


load_dotenv()

geolocator = Nominatim(user_agent='PYSAM_APP')

file_cache = {}

def download_weather_data(address):
        location = geolocator.geocode(address)
        working_directory = "runtime_tmp/PySAM Downloaded Weather Files"

        resource_getter = rT.FetchResourceFiles(
            tech='solar', 
            nrel_api_key=os.getenv("NREL_API_KEY"), 
            nrel_api_email=os.getenv("NREL_API_EMAIL"),
            resource_dir=working_directory)
        get_result = resource_getter.fetch([(location.longitude, location.latitude)])
        result_dict = get_result.resource_file_paths_dict
        weather_file_name = result_dict[(location.longitude, location.latitude)]
        print('\nResults Dict', result_dict)
        print('\nWeather File', weather_file_name)

        file_content = pd.read_csv(weather_file_name)
        file_cache[address] = file_content

        os.remove(weather_file_name)
        for file in os.listdir(working_directory):
            if file.endswith('.json'):
                 os.remove(f"{working_directory}/{file}")


def get_weather_file(address='1600 Pennsylvania Ave NW, Washington, DC 20500'):
    if address not in file_cache:
        download_weather_data(address)
    print('\nFile Cache', file_cache.keys())
    return file_cache[address]
