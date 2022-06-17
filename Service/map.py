# from .point import MapPoint
from .functions import getDirectionsFromAddress, getDirectionsFromLatLng, getLatLng, getPlaceName
from .point import MapPoint

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
            return {'distance': distance, 'duration': duration, 'data': data}
        return 'Error'

    def getDirectionsFromLatLng(self, origin: MapPoint, destination: MapPoint, profile='mapbox/driving'):

        response = getDirectionsFromLatLng(origin, destination, profile)
        distance = response['features']['distance']
        duration = response['features']['duration']

        return {'distance': distance, 'duration': duration, 'data': response}
