from django.contrib import admin

# Register your models here.

from .models import User, Vehicle, Drive


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "email",
                    "sex", "phone", "country", "user_type", 'status')
    search_fields = ("first_name", "last_name", "email",
                     "sex", "country", "user_type", 'status')
    list_display_links = ("id", "email", "username")

    readonly_fields = ("password",)

    list_filter = ("first_name", "last_name", "email")


admin.site.register(User, UserAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ("user", "driver_plate_number",
                    "car_color", "max_place", "nbp", "car_type", "car_brand")
    search_fields = ("user", "driver_plate_number",
                     "car_color", "car_type", "car_brand")


admin.site.register(Vehicle, VehicleAdmin)


class DriveAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'updated', 'created')

    fieldsets = (
        ('Vehicle', {
            "fields": ('vehicle',)
            }
        ),
        ('displacement_info', {
            "fields": ('origin', 'destination')
            }
        ),
        ('Date', {"fields": ('date', 'updated', 'created')})
    )
    list_display = ("vehicle", 'origin', 'destination')
    search_fields = ("vehicle", 'origin', 'destination')


admin.site.register(Drive, DriveAdmin)
