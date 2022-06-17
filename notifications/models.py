from pyexpat import model
from django.db import models

from django.contrib.auth import get_user_model
from map.models import UserBookPlace
from users.models import Vehicle

# Create your models here.


User = get_user_model()

class UserNotification(models.Model):


    user = models.ForeignKey(User,on_delete=models.CASCADE)
    msg = models.CharField(max_length=500)
    sender = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):

        return f'{self.user} Notification'

# https://app.getpostman.com/join-team?invite_code=9a50f8adddddfab7b2dcb487dbcf3d43

class DriverNotification(models.Model):

    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    msg = models.CharField(max_length=500)
    sender = models.ForeignKey(UserBookPlace,on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f'{self.vehicle.user} Notifications'