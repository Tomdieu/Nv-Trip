from django.contrib import admin

from .models import Trip, UserPosition, UserHistory,UserBookPlace,DriverTransportPassenger

# Register your models here.


class TripAdmin(admin.ModelAdmin):

    readonly_fields = ("created", "date")

    fieldsets = ((None, {"fields": ("user",)}),
                 ("Origin", {"fields": ("origin_name", "origin_lat", "origin_lng")}), ("Destination", {
                     "fields": ("destination_name", "destination_lat", "destination_lng")}),
                 ("Trip Additional Information", {"fields": (
                     "type_of_transport",)}),
                 ("Date", {"fields": ("date", "created")}))

    list_display = ("id", "user", "origin_name", "destination_name",
                     "type_of_transport", "date")

    search_fields = ("user", "origin_name", "destination_name",
                     "type_of_transport", "date",)

    list_display_links = ("id", "user")


admin.site.register(Trip, TripAdmin)


class UserPositionAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {"fields": ("user",)}),
        ("User Coordinate", {"fields": ("lat", "lng", "ip_address")}),
        ("Date", {"fields": ("date", "date_created")})
    )

    readonly_fields = ("date", "date_created")

    list_display = ("id", "user", "lat", "lng", "date")

    list_display_links = ("id", "user")

    search_fields = ("user",)


admin.site.register(UserPosition, UserPositionAdmin)


class UserHistoryAdmin(admin.ModelAdmin):

    readonly_fields = ("date_created", "date")

    fieldsets = (
        (None, {
            "fields": (
                "user",
            ),
        }),
        ("History Information", {
         "fields": ("search_place", "type", "lat", "lng")}),
        ("User Information", {"fields": ("country", "city")}),
        ("Date", {"fields": ("date", "date_created")})
    )

    list_display = ("id", "user", "search_place", "country", "date")

    search_fields = ("user", "search_place")

    list_display_links = ("id", "user")


admin.site.register(UserHistory, UserHistoryAdmin)

admin.site.register(UserBookPlace)

admin.site.register(DriverTransportPassenger)