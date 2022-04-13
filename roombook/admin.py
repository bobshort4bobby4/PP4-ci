from django.contrib import admin
from .models import Room, RoomType, Booking
# Register your models here.


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'price', 'occupancy')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'type', 'booked', 'occupied')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_number',  'check_in', 'check_out', 'is_active')

