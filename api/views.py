from django.shortcuts import render

# Create your views here.

# importing the rest_framwork classes

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins,viewsets

from map.models import DriverTransportPassenger, Trip, UserBookPlace, UserHistory, UserPosition


# importing our model serialize
from . serializers import DriverTransportPassengerSerializers, TripSerializers, UserBookPlaceSerializers, UserHistorySerializers, UserPositionSerializers, UserSerializers, VehicleSerializers


#importing our different models
from django.contrib.auth import get_user_model
from users.models import Vehicle

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    
    
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers

class UserPositionViewSet(viewsets.ModelViewSet):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializers
    
class UserHistoryViewSet(viewsets.ModelViewSet):
    queryset = UserHistory.objects.all()
    serializer_class = UserHistorySerializers
    
class UserBookPlaceViewSet(viewsets.ModelViewSet):
    queryset = UserBookPlace.objects.all()
    serializer_class = UserBookPlaceSerializers
    
class DriverTransportPassengerViewSet(viewsets.ModelViewSet):
    queryset = DriverTransportPassenger.objects.all()
    serializer_class = DriverTransportPassengerSerializers
    