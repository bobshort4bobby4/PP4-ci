
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView , View, TemplateView, FormView, CreateView
from .models import Room, RoomType, Booking
from forms.forms import AvailabilityForm
from django.contrib import messages
from booking_code.check_availability import check_availability
from datetime import date, datetime
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

class AvailabilityView(View):
    # template_name = 'roombook/book_1.html'
    form_class = AvailabilityForm

    def get(self, request, *args, **kwargs):
        type = self.kwargs.get('type', None)
        desc = RoomType.objects.get(type=type)
       
     
       
        Room_Types = ['Single', 'Queen', 'Double']
        if  type in Room_Types:
                form = AvailabilityForm()
                context = {
                 'type': type,
                 'form': form,
                 'desc': desc,

                }
                return render(request, 'roombook/book_1.html', context)
        else:
                messages.warning(request, 'That size unit does not exist..')
                return redirect(reverse('home:home'))

        
       
    def post(self, request, *args, **kwargs):
        
        type = self.kwargs.get('type', None)
        if type == 'Single':      # convert to int to match type of type_id in table
            typeint = 1
        elif type == 'Queen':
            typeint = 2
        elif type == 'Double':
            typeint = 3
        else:
            messages.warning(request, 'That size unit does not exist..')
            return redirect(reverse('roombook:home'))
            


        
        room_list = Room.objects.filter(type=typeint)   # get all instances of room type with the chosen class
        # unit = unit_list[0]   # get first first instance just to test if I can make a booking entry

        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
        else:
            messages.warning(request, 'Form not valid')
            return redirect( reverse('roombook:book_1',kwargs={'type':type}))
        
        available_rooms = [] # empty list to hold units that have availability for desired dates
        
        


        # check dates are chronological correct
        if data['check_in'] < date.today() or data['check_out'] < data['check_in']:
            messages.warning(request, 'Please enter a valid set of dates')
            return redirect( reverse('roombook:book_1',kwargs={'type':type}))
        else:
            for room in room_list:
                if check_availability(room, data['check_in'], data['check_out']):
                    available_rooms.append(room) # if unit is returned from check_availability function add to list

        if len(available_rooms) > 0: #if there is at least one room available 
            room = available_rooms[0]
            booking = {
                'room_number':str(room),
                'check_in':form.data['check_in'],
                'check_out':form.data['check_out'],
                'is_active':True,

            }
        
            # convert dict to json string
            with open("context.json", "w") as outfile:
                json.dump(booking, outfile)

            booking= {
                'context':outfile,
            }

            # send to book template
            return redirect('/roombook/book/<booking>/', booking)
                      
                                     
        else:
                messages.warning(request, 'All of this size of unit are booked!! Try another one')
                return redirect(reverse('home:home'))

               

class BookView(View):
    model = Booking
    template_name = 'roombook/book.html'

    def get(self, request, *args, **kwargs):
        outfile = self.kwargs.get('context', None)
        # convert json file
        with open('context.json') as json_file:
            data = json.load(json_file)
        
        # check occupancy rate for checkin date
        bookings = Booking.objects.all()
        rooms = Room.objects.all()
        bookedrooms = []
        y = int(data['check_in'][0:4])
        m = int(data['check_in'][5:7])
        d = int(data['check_in'][8:10])
         
        cin = date(y, m, d)  
        for room in rooms:
            for booking in bookings:
                if booking.room_number_id == room.room_number:
                    if cin >= booking.check_in:
                        if cin <= booking.check_out:
                            bookedrooms.append(room)

        countbookedrooms = int(len(bookedrooms))
        counttotalroom = Room.objects.all().count()
        # if occupancy rate below 60% set sale flag to true
        occrate = (countbookedrooms/counttotalroom)*100
        if (occrate) < 50:
            sale_flag = True
        else:
            sale_flag = False

        context = {
            'type':data,
            'sale_flag':sale_flag,
        }
        return render(request, self.template_name, context)
       


   
    def post(self, request, *args,**kargs):
        # check if user logged in
        if not request.user.is_authenticated :
            messages.error(request, 'Please sign in to make a Booking .')
            return redirect(reverse('home:home'))

        #convert json file
        outfile = self.kwargs.get('context', None)
        with open('context.json') as json_file:
            booking_data = json.load(json_file)

        # get instance of Room
        room = Room.objects.get(room_number=booking_data['room_number'])

        booking = Booking.objects.create(
                        user=request.user,
                        room_number=room,
                        check_in=booking_data['check_in'],
                        check_out=booking_data['check_out'],
                        is_active=True
                    )
        booking.save()   # make the booking
        
        messages.success(request, f"Thank you for booking room { booking_data['room_number'] } from { booking_data['check_in'] } to {booking_data['check_out'] }")
        return redirect(reverse('home:home'))
           

