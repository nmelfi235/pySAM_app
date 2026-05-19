import os
import pickle
from dotenv import load_dotenv

from geopy.geocoders import Nominatim
import PySAM.ResourceTools as rT


load_dotenv()

geolocator = Nominatim(user_agent='PYSAM_APP')

file_cache = {}

def download_weather_data(address):
        location = geolocator.geocode(address)

        resource_getter = rT.FetchResourceFiles(
            tech='solar', 
            nrel_api_key=os.getenv("NREL_API_KEY"), 
            nrel_api_email=os.getenv("NREL_API_EMAIL"),
            resource_dir='runtime_tmp/PySAM Downloaded Weather Files')
        get_result = resource_getter.fetch([(location.longitude, location.latitude)])
        result_dict = get_result.resource_file_paths_dict
        weather_file_name = result_dict[(location.longitude, location.latitude)]

        with open(weather_file_name, 'rb') as file:
             file_content = pickle.load(file)
             file_cache[address] = file_content

        os.remove(weather_file_name)

def get_weather_file(address):
    if address not in file_cache:
        download_weather_data(address)
    return file_cache[address]