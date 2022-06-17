from Service.map import MapPoint
from Service.map import MapServices

point = MapPoint(3, 4)
print(point['lat']*point['lng'])

lon, lat = 11.520526, 3.864768
p = MapPoint(lat, lon)

name = MapServices().getPlaceName(p)

print(name)

print(MapServices().getLatLng(name))

# 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