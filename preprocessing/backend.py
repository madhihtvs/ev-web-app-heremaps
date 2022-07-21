import pandas as pd
import requests
import flexpolyline as fp

def get_coordinates(location):
    """Getting coordinates from address"""
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    location_format = location.replace(" ", "+")
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={location_format}&apiKey={API}"

    resp = requests.get(url=url)
    data = resp.json()

    return data


def get_address(lat, lon):
    """Getting address from coordinates to be added to marker"""
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://revgeocode.search.hereapi.com/v1/revgeocode?at={lat}%2C{lon}&apiKey={API}&lang=en-US"
    
    resp = requests.get(url=url)
    data = resp.json()
 
    address = data["items"][0]['address']['label']
    return address


def get_POI(lat, lon, radius):
    """Getting Points of Interest when specified latitude, longitude and radius"""
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://discover.search.hereapi.com/v1/discover?limit=20&q=eat-drink,going-out,sights-museums,shopping,leisure-outdoor&in=circle:{lat},{lon};r={radius}&apiKey={API}"
    
    resp = requests.get(url=url)
    data = resp.json()


    POI = []
    for i in range(len(data['items'])):
        name = data["items"][i]['title']
        category = data["items"][i]['categories'][0]['name']
        lat = data["items"][i]['position']['lat']
        lng = data["items"][i]['position']['lng']
        POI.append([name, category, lat, lng])
    
    df = pd.DataFrame(POI, columns = ["Name","Category","Latitude", "Longitude"])

    return df



def get_Hotel(lat, lon):
    """Getting places of accommmodation given a latitude and longitude with a specific radius of 5000km"""
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://discover.search.hereapi.com/v1/discover?limit=20&q=accommodation&in=circle:{lat},{lon};r=5000&apiKey={API}"
    
    resp = requests.get(url=url)
    data = resp.json()


    POI = []
    for i in range(len(data['items'])):
        name = data["items"][i]['title']
        category = data["items"][i]['categories'][0]['name']
        lat = data["items"][i]['position']['lat']
        lng = data["items"][i]['position']['lng']
        POI.append([name, category, lat, lng])

    df = pd.DataFrame(POI, columns = ["Name","Category","Latitude", "Longitude"])
    return df


    
def get_route(orig_lat, orig_lon, dest_lat, dest_lon):
    """Get polyline path between origin and destination. Also return total distance and total time together with list of coordinates"""
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://router.hereapi.com/v8/routes?transportMode=scooter&scooter[allowHighway]=true&origin={orig_lat},{orig_lon}&destination={dest_lat},{dest_lon}&return=polyline,summary&apikey={API}"
    response = requests.request("GET", url)
    data = response.json()
    polyline = data["routes"][0]['sections'][0]['polyline']
    lst = fp.decode(polyline)
    distance = data['routes'][0]['sections'][0]['summary']['length']
    distance = distance / 1000
    time = data['routes'][0]['sections'][0]['summary']['duration']
    return lst, distance, time


def get_route_short(orig_lat, orig_lon, dest_lat, dest_lon):
    """Get polyline path between origin and destination which is shorter than the default. Also return total distance and total time together with list of coordinates"""
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://router.hereapi.com/v8/routes?transportMode=car&routingMode=short&origin={orig_lat},{orig_lon}&destination={dest_lat},{dest_lon}&return=polyline,summary&apikey={API}"
    response = requests.request("GET", url)
    data = response.json()
    polyline = data["routes"][0]['sections'][0]['polyline']
    lst = fp.decode(polyline)
    distance = data['routes'][0]['sections'][0]['summary']['length']
    distance = distance / 1000
    time = data['routes'][0]['sections'][0]['summary']['duration']
    return lst, distance, time


def get_route_many(*points):
    """Get polyline path between multiple points (No Limit). Also return total distance and total time together with list of coordinates"""
    
    string = ""
    lst = points[0]
    orig_lat = lst[0][0]
    orig_lon = lst[0][1]
    dest_lat = lst[-1][0]
    dest_lon = lst[-1][1]
    points = points[0]
    del points[0]
    del points[-1]
    for i in points:
        lat = i[0]
        lng = i[1]
        string += f"&via={lat},{lng}"
    
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://router.hereapi.com/v8/routes?transportMode=scooter&origin={orig_lat},{orig_lon}&destination={dest_lat},{dest_lon}{string}&return=polyline,summary&apikey={API}"
    response = requests.request("GET", url)
    data = response.json()
    polyline = []
    distance = 0
    time = 0
    for i in range(len(lst)+1):
        polyline_leg = data["routes"][0]['sections'][i]['polyline']
        lst = fp.decode(polyline_leg)
        polyline.extend(lst)
        distance += data['routes'][0]['sections'][i]['summary']['length']
        time += data['routes'][0]['sections'][i]['summary']['duration']
    distance = distance / 1000
    return polyline, distance, time


def get_route_many_short(*points):
    """Get polyline path between multiple points (No Limit) which is shorter than balanced route. Also return total distance and total time together with list of coordinates"""
    string = ""
    lst = points[0]
    orig_lat = lst[0][0]
    orig_lon = lst[0][1]
    dest_lat = lst[-1][0]
    dest_lon = lst[-1][1]
    points = points[0]
    del points[0]
    del points[-1]
    for i in points:
        lat = i[0]
        lng = i[1]
        string += f"&via={lat},{lng}"
    
    API = "FIAqwEHj3qFBbqhhKYS4PYfaeR_8thfqZiabEhWhyc4"
    url = f"https://router.hereapi.com/v8/routes?transportMode=car&routingMode=short&origin={orig_lat},{orig_lon}&destination={dest_lat},{dest_lon}{string}&return=polyline,summary&apikey={API}"
    response = requests.request("GET", url)
    data = response.json()
    polyline = []
    distance = 0
    time = 0
    for i in range(len(lst)+1):
        polyline_leg = data["routes"][0]['sections'][i]['polyline']
        lst = fp.decode(polyline_leg)
        polyline.extend(lst)
        distance += data['routes'][0]['sections'][i]['summary']['length']
        time += data['routes'][0]['sections'][i]['summary']['duration']

    distance = distance / 1000

    return polyline, distance, time



def get_weather(lat, lon):
    
    doc = {
        0: "Clear sky",
        1: "Mainly clear, partly cloudy, and overcast",
        2: "Mainly clear, partly cloudy, and overcast",
        3: "Mainly clear, partly cloudy, and overcast",
        45: "Fog and depositing rime fog",
        48: "Fog and depositing rime fog",
        51: "Drizzle: Light, moderate, and dense intensity",
        53: "Drizzle: Light, moderate, and dense intensity",
        55: "Drizzle: Light, moderate, and dense intensity",
        56: "Freezing Drizzle: Light and dense intensity",
        57: "Freezing Drizzle: Light and dense intensity",
        61: "Rain: Slight, moderate and heavy intensity",
        63: "Rain: Slight, moderate and heavy intensity",
        65: "Rain: Slight, moderate and heavy intensity",
        66: "Freezing Rain: Light and heavy intensity",
        67: "Freezing Rain: Light and heavy intensity",
        71: "Snow fall: Slight, moderate, and heavy intensity",
        73: "Snow fall: Slight, moderate, and heavy intensity",
        75: "Snow fall: Slight, moderate, and heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight, moderate, and violent",
        81: "Rain showers: Slight, moderate, and violent",
        82: "Rain showers: Slight, moderate, and violent",
        85: "Snow showers slight and heavy",
        86: "Snow showers slight and heavy",
        95: "Thunderstorm: Slight or moderate"
    }

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
    resp = requests.get(url=url)
    data = resp.json()
    weather_code = int(data["current_weather"]["weathercode"])
    return doc[weather_code]
