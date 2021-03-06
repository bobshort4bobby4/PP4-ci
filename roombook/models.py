from django.db import models
from django.conf import settings
from datetime import datetime, date


class markoutdatedasinactive(models.Manager):
    """ 
    determines if the booking is past-tense and changes the is_active field to false if so
    """

    def set_inactive(self,bookings):
        today = date.today()

        for booking in bookings:
            if booking.check_out < today:
                booking.is_active = False
                booking.save()
        #this_booking what is that about 
        return bookings

    def all(self):
        bookings = super().all() # is this ordinary all or my all or are they now the same thing?
        bookings = self.set_inactive(bookings)
        return bookings

###  can i filter the booking to only include records that are active can i chain methods, tryit out 
### when is this activated ? everytime the model is accessed? everytime the all is called?
### is it possible to activate only once per day at say mdnight  




class RoomType(models.Model):
    Room_Types = (
        ('Single', 'Single'),
        ('Queen', 'Queen'),
        ('Double', 'Double'),
    )

    type = models.CharField(max_length=6, null=False, choices= Room_Types)
    description = models.TextField(max_length=250, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    occupancy = models.IntegerField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.type}'

class Room(models.Model):

    room_number = models.IntegerField()
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    occupied = models.BooleanField(default=False)
   

    def __str__(self):
        return f'{self.room_number}'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)
    is_active = models.BooleanField(default= True)


    objects = markoutdatedasinactive()

    def __str__(self):
        return f"{self.user} has booked  Room {self.room_number} from {self.check_in} to {self.check_out}"


    