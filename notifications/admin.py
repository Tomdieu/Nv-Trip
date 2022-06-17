from django.contrib import admin

from .models import UserNotification,DriverNotification

# Register your models here.

class UserNotificationsAdmin(admin.ModelAdmin):

    list_display = ('user','msg','sender','read','created',)


admin.site.register(UserNotification,UserNotificationsAdmin)


class DriverNotificationsAdmin(admin.ModelAdmin):

    list_display = ('vehicle','msg','sender','accepted','created')

admin.site.register(DriverNotification,DriverNotificationsAdmin)