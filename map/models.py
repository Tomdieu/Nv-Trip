from django.db import models

from users.models import User,Vehicle

from django.utils.translation import gettext_lazy as _

# importing out service package
import Service
from Service import getLatLng,getPlaceName

# Create your models here.


class Trip(models.Model):

    TYPE = (
        ("DRIVING", "DRIVING"),
        ("WALKING", "WALKING"),
        ("CYCLING", "CYCLING")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin_lat = models.FloatField("Origin Latitude")
    origin_lng = models.FloatField("Origin Longitude")
    origin_name = models.CharField("Origin", max_length=50)
    destination_lat = models.FloatField("Destination Latitude")
    destination_lng = models.FloatField("Destination Longitude")
    destination_name = models.CharField("Destination", max_length=50)
    # distance = models.IntegerField("Distance Between the Origin and Destination")
    # walk_time = models.IntegerField("Walking Time")
    # car_time = models.IntegerField("Car Time")
    # bike_time = models.IntegerField("Bike Time")
    type_of_transport = models.CharField(
        "Mode Of Transport", choices=TYPE, max_length=30)
    # transport_cost = models.IntegerField("Cost Of Transport", default=0)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _("trip")
        verbose_name_plural = _("Trips")
        ordering = ["date"]

    def getProfile(self):
        if self.type_of_transport == 'DRIVING':
            profile = 'mapbox/driving'
        elif self.type_of_transport == 'WALKING':
            profile = 'mapbox/walking'
        elif self.type_of_transport == 'CYCLING':
            profile = 'mapbox/cycling'
        else:
            profile = 'mapbox/driving'

        return profile

    def getOriginLatLng(self):
        data = getLatLng(self.origin_name)
        return data['coordinates']

    def getDestinationLatLng(self):
        data = getLatLng(self.destination_name)
        return data['coordinates']

    def getInfo(self):
        profile = self.getProfile()
        lngLat1 = self.getOriginLatLng()
        lngLat2 = self.getDestinationLatLng()

        point1 = Service.MapPoint(lat=lngLat1[1],lng=lngLat1[0])
        point2 = Service.MapPoint(lat=lngLat2[1],lng=lngLat2[0])

        direction = Service.getDirectionsFromLatLng(point1, point2,profile)

        return direction

    def getDistance(self):

        info = self.getInfo()

        if info:
            return info['features']['distance'] / 1000
        return None

    def getTime(self):
        info = self.getInfo()

        if info:
            return info['features']['duration']
        return None

class UserPosition(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.FloatField("Latitude")
    lng = models.FloatField("Longitude")
    ip_address = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("user position")
        verbose_name_plural = _("user positions")


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_place = models.CharField("Place search", max_length=250)
    type = models.CharField("Type", max_length=50)
    lat = models.FloatField("Latitude")
    lng = models.FloatField("Longitude")
    country = models.CharField("Country", max_length=100)
    city = models.CharField("City", max_length=50)
    date = models.DateField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["date"]


class UserBookPlace(models.Model):

    PAYMENT_OPTION = (
        ("CASH","CASH"),
        ('MOBILE MONEY','MOBILE MONEY'),
        ('ORANGE MONEY','ORANGE MONEY')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    price = models.CharField('Price (XAF)',max_length=5)
    number_of_place = models.IntegerField(default=1)
    payment_option = models.CharField(max_length=40,choices=PAYMENT_OPTION)
    place_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-place_date"]


    def __str__(self):

        return f'{self.user} {self.origin}:{self.destination}'
    

class DriverTransportPassenger(models.Model):

    TYPE = (
        ('accept','accept'),
        ('refuse','refuse')
    )

    booked = models.ForeignKey(UserBookPlace, on_delete=models.CASCADE,blank=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,blank=False)
    accept = models.CharField(max_length=20,choices=TYPE)
    date = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]