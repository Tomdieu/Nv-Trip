from django.conf import settings
from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.
from .validators import validate_dob,min_place,check_plc


class User(AbstractUser):

    ONLINE = 'online'
    OFFLINE = 'offline'

    STATUS = (
        (ONLINE,'online'),
        (OFFLINE,'offline'),
    )

    USER_TYPE = (
        ("PASSENGER", "PASSENGER"),
        ("DRIVER", "DRIVER")
    )

    SEX = (
        ("M", "M"),
        ("F", "F")
    )

    email = models.EmailField("Email Address", unique=True)
    sex = models.CharField(
        "Sex", choices=SEX, max_length=2, null=False, blank=False)
    phone = models.CharField(
        "Phone Number", max_length=20, blank=False, null=False)
    country = models.CharField(
        "country", max_length=40, blank=False, null=False)
    user_type = models.CharField(
        "Who Are You ?", max_length=20, choices=USER_TYPE, null=False, blank=False)
    status = models.CharField('status',max_length=10,choices=STATUS,default=ONLINE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", 'sex',"phone", "country"]

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["date_joined"]


class Vehicle(models.Model):

    ONLINE = 'online'
    OFFLINE = 'offline'

    STATUS = (
        (ONLINE,'online'),
        (OFFLINE,'offline'),
    )

    COLORS = (
        ("YELLOW", "YELLOW"),
        ("BLACK", "BLACK"),
        ("WHITE", "WHITE"),
        ("BLUE", "BLUE"),
        ("BROWN", "BROWN"),
        ("RED", "RED"),
        ("GREEN", "GREEN"),
    )

    VEHICLE_TYPE = (
        ('CAR','CAR'),
        ('BUS','BUS')
    )

    CAR_TYPE = (
        ("TOYOTA", "TOYOTA"),
        ("HONDAS", "HONDAS"),
        ("MERCEDES", "MERCEDES"),
        ("BMW", "BMW"),
        ("HYUNDAI", "HYUNDAI"),
        ("LEXUS", "LEXUS"),
        ("PEUGEOT", "PEUGEOT"),
        ("ROLL ROYCE", "ROLL ROYCE"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_plate_number = models.CharField(
        "License Plate", max_length=7, unique=True)
    car_color = models.CharField("Car Color", max_length=20, choices=COLORS)
    max_place = models.IntegerField("Maximum number of place in car",validators=[min_place])
    nbp = models.IntegerField("Current Number Of Place Available",default=1,validators=[check_plc])
    car_type = models.CharField("Vehicle Type", max_length=20, choices=VEHICLE_TYPE)
    car_brand = models.CharField(max_length=30,choices=CAR_TYPE)    
    lat = models.CharField('Latitude',max_length=20)
    lng = models.CharField('Longitude',max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField('status',max_length=10,choices=STATUS,default=OFFLINE)


    def __str__(self):
        return f'{self.driver_plate_number}'


class Drive(models.Model):
    
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    origin = models.CharField('Origin',max_length=50)
    destination = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return f'{self.vehicle}'
    
    class Meta:
        verbose_name = _("drive")
        verbose_name_plural = _("drives")
        ordering = ["created"]