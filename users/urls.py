from django.urls import path

from . import views
from core import views as vw
from notifications.views import user_notifications

app_name = 'user'

urlpatterns = [
	path('',views.index,name="user_index"),
 	path('logout/',views.signout,name="logout"),
 	# path('find-path/',vw.find_path,name="find-path"),
	 path('profile/',views.profile,name="profile"),
 	path('path/',vw.FindPath.as_view(),name="path"),
 	path('choose/',vw.BookPlace.as_view(),name="choose"),
 	path('choose/select-driver/',vw.SelectDriver.as_view(),name="choose-driver"),
 	path('driver/choose/',vw.SelectOriginDestination.as_view(),name='driver-choose'),
 	path('driver/drive/<drive_id>/',vw.driver,name='drive'),
 	path('driver/create-vehicle/',vw.createVehicle,name='create-vehicle'),
	path('drive/update-drive-information/',vw.update_driver_drive,name='update-drive'),
	path('vehicle/update-places',vw.update_vehicle_place,name='update-place'),
	path('settings/',views.gotoSettings,name="settings"),
	path('notifications/',user_notifications,name="user_notifications"),
	path('userbookplaced/',views.user_placedbook,name="placed_book"),
	path('verifypassword/',views.verify_password,name="verify_password"),
	path('update_user_password/',views.update_user_password,name="update_user_password"),
	path('update_user_info/',views.updateUserInfo,name='updateUserInfo'),
	path('create_vehicle/',views.create_vehicle,name="create_vehicle"),
	path('delete_account/',views.deleteAccount,name="delete_account"),
	path('checkEmail/',views.checkIfEmailExists,name="checkEmail"),
	path('checkUserName/',views.checkIfUserNameExists,name="checkUserName"),
	path('createUser/',views.createUser,name="createUser"),
]