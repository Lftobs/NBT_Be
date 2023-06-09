import requests
from math import radians, sin, cos, sqrt, atan2

class FoodTrucksLocation:
    def __init__(self):
        self._base_url = 'https://api.geoapify.com/v1/geocode/'
        self._base_url1 = 'https://data.sfgov.org/resource/rqzj-sfat.json'
        self._api_key = '4380b87f40a8465facdeac8254117a28'
        
    def get_latlong(self, address):
        url = f'{self._base_url}search?text={address}&limit=1&apiKey={self._api_key}'
        res = requests.get(url)
        if res.status_code == 200:
             data = res.json()
             result = data['features'][0]
             lat = result['geometry']['coordinates'][1]
             long = result['geometry']['coordinates'][0]
             return [lat, long]
        return {'status': res.status_code,'error': res.reason}
             
    def get_distance(self, inp_lat, inp_long, api_lat, api_long):
        inp_lat, inp_long, api_lat, api_long = float(inp_lat), float(inp_long), float(api_lat), float(api_long)
        
        inp_lat, inp_long, api_lat, api_long = map(radians, [inp_lat, inp_long, api_lat, api_long])
        radius = 6371
        dist_lat = api_lat - inp_lat
        dist_long = api_long - inp_long
        a = sin(dist_lat/2)**2 + cos(inp_lat) *cos(api_lat) * sin(dist_long/2)**2
        coord = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = radius * coord
        return distance
        
    def get_food_trucks_data(self):
        res = requests.get(self._base_url1)
        if res.status_code == 200:
            data = res.json()
            return data
        return {'status': res.status_code,'error': res.reason}


food_trucks = FoodTrucksLocation()
