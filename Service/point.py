from mapbox import Directions

from .functions import getPlaceName, getLatLng
ACCESS_TOKEN = "pk.eyJ1IjoiaXZhbnRvbSIsImEiOiJjbDJnMGlwNnYwZm9zM2duYnQ0a3c2bXFvIn0.x29uaFl79xgLW6nCs15JWw"
access_token = ACCESS_TOKEN


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
