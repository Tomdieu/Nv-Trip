import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator

from django.contrib.auth import get_user_model
# from users.routing import websocket_urlpatterns
from users.consumers import UserConsumer,VehicleConsumer
from notifications.consumers import UserNotificationsConsumer,DriverNotificationsConsumer
import notifications.routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^user/$', UserConsumer.as_asgi()),
                    url(r'^vehicle/(?P<id>\w+)/$',VehicleConsumer.as_asgi()),
                ]+notifications.routing.websocket_urlpatterns
            )
        )
    )
})