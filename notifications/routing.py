from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^drivernotifications/(?P<id>\w+)/$',consumers.DriverNotificationsConsumer.as_asgi()),
    re_path(r'^usernotifications/(?P<id>\w+)/$',consumers.UserNotificationsConsumer.as_asgi())
]