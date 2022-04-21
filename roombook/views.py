
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView , View, TemplateView, FormView, CreateView
from .models import Room, RoomType, Booking
from forms.forms import AvailabilityForm
from django.contrib import messages
from booking_code.check_availability import check_availability
from datetime import date
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

class AvailabilityView(View):
    # template_name = 'roombook/book_1.html'
    form_class = AvailabilityForm

    def get(self, request, *args, **kwargs):
        type = self.kwargs.get('type', None)
        Room_Types = ['Single', 'Queen', 'Double']
        if  type in Room_Types:
                form = AvailabilityForm()
                context = {
                 'type': type,
                 'form': form
                }
                return render(request, 'roombook/book_1.html', context)
        else:
                messages.warning(request, 'That size unit does not exist..')
                return redirect(reverse('home:home'))

        
       
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated :
        #     messages.error(request, 'Please sign in to make a Booking .')
        #     return redirect(reverse('roombook:home'))


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
            context = {
                # 'user':str(self.request.username),
                'room_number':str(room),
                'check_in':form.data['check_in'],
                'check_out':form.data['check_out'],
                'is_active':True,

            }
        
            # convert dict to json string
            with open("context.json", "w") as outfile:
                json.dump(context, outfile)

          
            
            # context = json.dumps(context)
            
            # with open('context.json') as json_file:
            #     data = json.load(json_file)
                
            # return render(request,'roombook/book.html',context)
            return redirect('/roombook/book/<context>', {'context':outfile})

            # django docs
            # redirect(to, *args, permanent=False, **kwargs)¶
    #         def my_view(request):
    # ...
    # return redirect('some-view-name', foo='bar')                          
                                     
        else:
                messages.warning(request, 'All of this size of unit are booked!! Try another one')
                return redirect(reverse('home:home'))

               

class BookView(View):
    model = Booking
    template_name = 'roombook/book.html'

    def get(self, request, *args, **kwargs):
        outfile = self.kwargs.get('context', None)
        with open('context.json') as json_file:
            data = json.load(json_file)
        return render(request, self.template_name, {'type':data})


   
    def post(self, request, *args,**kargs):
        if not request.user.is_authenticated :
            messages.error(request, 'Please sign in to make a Booking .')
            return redirect(reverse('home:home'))

        outfile = self.kwargs.get('context', None)
        with open('context.json') as json_file:
            booking_data = json.load(json_file)

        u = request.user.username
        room = Room.objects.get(room_number=booking_data['room_number'])

        booking = Booking.objects.create(
                        user=request.user,
                        room_number=room,
                        check_in=booking_data['check_in'],
                        check_out=booking_data['check_out'],
                        is_active=True
                    )
        booking.save()   # make the booking
        # check_in = form.data['check_in']
        # check_out = form.data['check_out']
        messages.success(request, f"Thank you for booking room { booking_data['room_number'] } from { booking_data['check_in'] } to {booking_data['check_out'] }")
        return redirect(reverse('home:home'))
           

