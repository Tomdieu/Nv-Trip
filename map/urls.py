from os import name
from django.urls import path

from . import views

app_name = "map"

urlpatterns = [
    path("", views.LandingView.as_view(), name="map"),
    path("get_directions/", views.getDirections)
]
