from django.contrib import admin
from .models import Room, RoomType, Booking
from datetime import date, timedelta
# Register your models here.


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'price', 'occupancy_14_Days',  'occupancy_30_Days')

    def occupancy_14_Days(self,obj):
        today = date.today()
        # number of rooms of that type
        no_rooms = len(Room.objects.filter(type= obj))
        #total days it is possible to have booked for that room ie 100% occupancy
        tot_days = no_rooms*14
        # all rooms of that type
        rooms = Room.objects.filter(type= obj)
        # empty list to hold room ids, get room ids
        roomid =[]
        for room in rooms:
            roomid.append(room.id)
        # get all booking for that type of room
        bookings = Booking.objects.filter(room_number_id__in=roomid)
        # variable to store days actually booked in this period for this room type
        booked_days = 0
        # iterate through booking and count which days are booked for each room
        for booking in bookings:
            for day in range(0,14):
                dat =today + timedelta(days=day)
                if dat >= booking.check_in and dat < booking.check_out:
                    booked_days += 1

        occupancy_rate = str(    (booked_days/tot_days)*100)
        return occupancy_rate[0:4]


    def occupancy_30_Days(self,obj):
        today = date.today()
        # number of rooms of that type
        no_rooms = len(Room.objects.filter(type= obj))
        #total days it is possible to have booked for that room ie 100% occupancy
        tot_days = no_rooms*30
        # all rooms of that type
        rooms = Room.objects.filter(type= obj)
        # empty list to hold room ids, get room ids
        roomid =[]
        for room in rooms:
            roomid.append(room.id)
        # get all booking for that type of room
        bookings = Booking.objects.filter(room_number_id__in=roomid)
        # variable to store days actually booked in this period for this room type
        booked_days = 0
        # iterate through booking and count which days are booked for each room
        for booking in bookings:
            for day in range(0,30):
                dat =today + timedelta(days=day)
                if dat >= booking.check_in and dat < booking.check_out:
                    booked_days += 1

        occupancy_rate = str(    (booked_days/tot_days)*100)
        return occupancy_rate[0:4]



        




# model.objects.filter(pk__in=list_of_ids)
# def show_average(self, obj):
#         from django.db.models import Avg
#         result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
#         return result["grade__avg"]
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'type', 'booked', 'occupied')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_number',  'check_in', 'check_out', 'is_active')
    list_filter = ('is_active', 'room_number')

