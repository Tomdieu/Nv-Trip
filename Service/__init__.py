from mapbox import Directions # importing mapbox
from mapbox import Geocoder

ACCESS_TOKEN = "pk.eyJ1IjoiaXZhbnRvbSIsImEiOiJjbDJnMGlwNnYwZm9zM2duYnQ0a3c2bXFvIn0.x29uaFl79xgLW6nCs15JWw"
access_token = ACCESS_TOKEN

def Feature(address, coordinates):
    '''
        Returns
        --------
        {
            "type": "Feature",
            "properties": {"name": address},
            "geometry": {
                "type": "Point",
                "coordinates": coordinates
            }
        }
    '''
    return {
        "type": "Feature",
        "properties": {"name": address},
        "geometry": {
            "type": "Point",
            "coordinates": coordinates
        }
    }


def getLatLng(address, country="cm"):
    '''
        Parameter
        ---------

        address : string
            a valid address on the map

        Returns
        --------
        Return a dictionary having place_name,bbox,center,coordinates        

    '''
    geocoder = Geocoder(access_token=access_token)

    response = geocoder.forward(address, country=[country])

    if response.status_code in range(200, 299):
        data = response.json()
        return data
        # return {"place_name": data["features"][0]["place_name"], "bbox": data["features"][0]["bbox"], "center": data["features"][0]["center"], "coordinates": data["features"][0]["geometry"]["coordinates"]}

    return None


def getPlaceName(lat: int, lng: int):
    '''
        Returns
        ---------

        Return the dictionary having place_name,center,bbox,and coordinates
    '''
    geocoder = Geocoder(access_token=access_token)
    response = geocoder.reverse(lng, lat)
    if response.status_code in range(200, 299):
        data = response.json()
        print(data)
        # if data:
            # return {"place_name": data["features"][0]["place_name"], "center": data["features"][0]["center"], "bbox": data["features"][0]["bbox"], "coordinates": data["features"][0]["geometry"]["coordinates"]}
        # return {}
    return None


def getDirectionsFromAddress(address1: str, address2: str, profile='mapbox/driving'):
    '''

        parameters
        -----------
        address1 : string
            the name of the address1 

        address2 : string
            the name of the address2

        profile : string
            valid profile are mapbox/driving,mapbox/walking,mapbox/cycling


        Returns
        -----------

        Returns a Json having keys as 'type','features','properties'

    '''

    origin = Feature(address1, getLatLng(address1)['features'][0]['geometry']['coordinates'])

    destination = Feature(address2, getLatLng(address2)['features'][0]['geometry']['coordinates'])

    service = Directions(access_token=access_token)
    response = service.directions([origin, destination], profile)

    if response.status_code in range(200, 299):
        print(response.json())
        return 'Success', response.json()
    return 'Error', {}





class MapPoint:
    """Class MapPoint"""

    def __init__(self, lat=0, lng=0):
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        d = dict(lat=self.lat, lng=self.lng)
        return str(d)

    def __getitem__(self, it: str):
        """Return self.it"""
        return self.lat if it == "lat" else self.lng

    def _getInfo(self, point, profile):
        origin_info = getPlaceName(self.lat, self.lng)

        origin = {
            "type": "Feature",
            "properties": {"name": origin_info["place_name"]},
            "geometry": {
                "type": "Point",
                "coordinates": origin_info["coordinates"]
            }
        }

        destination_info = getPlaceName(point.lat, point.lng)

        destination = {
            "type": "Feature",
            "properties": {"name": destination_info["place_name"]},
            "geometry": {
                "type": "Point",
                "coordinates": destination_info["coordinates"]
            }
        }

        service = Directions(access_token=access_token)
        response = service.directions([origin, destination], profile)

        if response.status_code in range(200, 299):
            return 'Success', response.json()
        return 'Error', {}

    def distanceTo(self, point, profile="mapbox/driving"):
        """Find the distance between two points """
        data = self._getInfo(point, profile)

        if data[0] == 'Success':
            return data[1]['properties']['distance']

        return {}

    def durationTo(self, point, profile="mapbox/driving"):
        """Find the duration between two places"""

        data = self._getInfo(point, profile)

        if data[0] == 'Success':
            return data[1]['properties']['duration']

    def setLat(self, lat):
        self.lat = lat

    def selfLng(self, lng):
        self.lng = lng

def getDirectionsFromLatLng(point1:MapPoint, point2:MapPoint, profile='mapbox/driving'):
    """
    Parameter
    ---------
    point1 : MapPoint
        a point represented by lat,lng
    point2 : MapPoint
        a point represented by lat,lng
    profile : str
        valid profile are
        mapbox/driving,mapbox/walking,mapbox/cycling

    Returns
    ---------
    The directions between two points on the map having coordinates line,distance and duration
    """

    origin_info = getPlaceName(point1.lat, point1.lng)
    destination_info = getPlaceName(point2.lat, point2.lng)

    origin = Feature(origin_info['place_name'], origin_info['coordinates'])
    destination = Feature(
        destination_info['place_name'], destination_info['coordinates'])

    service = Directions(access_token=access_token)
    response = service.directions([origin, destination], profile)

    if response.status_code in range(200, 299):
        return response.json()
    return {}



class MapServices:

    def __init__(self, access_token="pk.eyJ1IjoiaXZhbnRvbSIsImEiOiJjbDJnMGlwNnYwZm9zM2duYnQ0a3c2bXFvIn0.x29uaFl79xgLW6nCs15JWw"):

        self.access_token = access_token

    def getLatLng(self, address, country='cm'):
        '''
            Returns
            --------

            Returns the latitude and longitude of a valid address 
        '''
        d = getLatLng(address, country)['coordinates']
        return MapPoint(d[0], d[1])

    def getPlaceName(self, point: MapPoint):
        '''
            Returns
            --------

            Return the place name from a lat,lng
        '''
        d = getPlaceName(point.lat, point.lng)['place_name']
        return d

    def getDirectionsFromName(self, origin: str, destination: str, profile='mapbox/driving'):
        '''
            Returns
            --------

            Returns the distance ,duration and dictionary having the different coodinates 
        '''
        response = getDirectionsFromAddress(origin, destination, profile)
        if response[0] == 'Success':
            data = response[1]
            distance = data['features']['distance']
            duration = data['features']['duration']
            return {'distance': distance, 'duration': duration, 'data': data,'more':response}
        return 'Error'

    def getDirectionsFromLatLng(self, origin: MapPoint, destination: MapPoint, profile='mapbox/driving'):

        response = getDirectionsFromLatLng(origin, destination, profile)
        distance = response['features']['distance']
        duration = response['features']['duration']

        return {'distance': distance, 'duration': duration, 'data': response}
