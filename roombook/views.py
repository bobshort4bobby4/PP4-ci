
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView , View, TemplateView
from .models import Room, RoomType, Booking
from forms.forms import AvailabilityForm
from django.contrib import messages
from booking_code.check_availability import check_availability
from datetime import date
# Create your views here.

# class Home(TemplateView):
#     template_name = "roombook/home.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['room_types'] = RoomType.objects.all()
#         return context
    # model = RoomType
    # template_name = 'roombook/home.html'
    # ordering = ['pk']


class AvailableForm(View):

        
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
                return redirect(reverse('roombook:home'))
                
        
        def post(self, request, *args, **kwargs):
            if not request.user.is_authenticated :
                messages.error(request, 'Please sign in to make a Booking .')
                return redirect(reverse('roombook:home'))


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
            
            available_rooms = [] # empty list to hold units that have availability for desires dates

            if data['check_in'] < date.today() or data['check_out'] < data['check_in']:
                messages.warning(request, 'Please enter a valid set of dates')
                return redirect( reverse('roombook:book_1',kwargs={'type':type}))
            else:
                for room in room_list:
                    if check_availability(room, data['check_in'], data['check_out']):
                        available_rooms.append(room) # if unit is returned from check_availability funstion add to list

            if len(available_rooms) > 0: #if there is at least one room available 
                room = available_rooms[0]
                booking = Booking.objects.create(
                    user=self.request.user,
                    room_number=room,
                    check_in=form.data['check_in'],
                    check_out=form.data['check_out'],
                )
                booking.save()   # make the booking
                check_in = form.data['check_in']
                check_out = form.data['check_out']
                messages.success(request, f'Thank you for booking room {room} from {check_in} to {check_out}')
                return redirect(reverse('roombook:home'))
            else:
                messages.warning(request, 'All of this size of unit are booked!! Try another one')
                return redirect(reverse('roombook:home'))



        

