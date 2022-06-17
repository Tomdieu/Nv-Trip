from django.urls import path,include


from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


router.register('users',views.UserViewSet)
router.register('vehicle',views.VehicleViewSet)
router.register('trips',views.TripViewSet)
router.register('user_position',views.UserPositionViewSet)
router.register('user_history',views.UserHistoryViewSet)
router.register('user_book_place',views.UserBookPlaceViewSet)
router.register('driver_transport_passenger',views.DriverTransportPassengerViewSet)


urlpatterns = [
    path('',include(router.urls))
]
