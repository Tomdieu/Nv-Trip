from mapbox import Geocoder, Directions
# from .point import MapPoint
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
        return {"place_name": data["features"][0]["place_name"], "bbox": data["features"][0]["bbox"], "center": data["features"][0]["center"], "coordinates": data["features"][0]["geometry"]["coordinates"]}

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
        return {"place_name": data["features"][0]["place_name"], "center": data["features"][0]["center"], "bbox": data["features"][0]["bbox"], "coordinates": data["features"][0]["geometry"]["coordinates"]}
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

    origin = Feature(address1, getLatLng(address1)['coordinates'])

    destination = Feature(address2, getLatLng(address2)['coordinates'])

    service = Directions(access_token=access_token)
    response = service.directions([origin, destination], profile)

    if response.status_code in range(200, 299):
        return 'Success', response.json()
    return 'Error', {}


def getDirectionsFromLatLng(point1, point2, profile='mapbox/driving'):
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
