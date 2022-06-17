from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from django.contrib.auth.decorators import login_required

from users.models import Vehicle
from .models import UserNotification,DriverNotification

@login_required
def user_notifications(request):

    template_name = 'user/notifications.html'
    context = {}

    users_vehicles = Vehicle.objects.filter(user=request.user)
    notifications = UserNotification.objects.filter(user=request.user)
    drivernotifications  = DriverNotification.objects.filter(vehicle__in=users_vehicles)
    context['notifications'] = notifications
    context['drivernotifications'] = drivernotifications

    return render(request,template_name,context)