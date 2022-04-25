""" 
roombook unit tests
"""


from django.test import TestCase, Client
from forms.forms import AvailabilityForm
from home.views import HomeView
from .models import RoomType, Room, Booking
from django.test import tag
from booking_code.check_availability import check_availability
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
import json


@tag('forms')
class TestAvailabilityForm(TestCase):

    def test_checkin_required(self):
        # create form field with blank value 
        form = AvailabilityForm({'check_in': ''})
        # check if form valid,error in correct field and correct error produced
        self.assertFalse(form.is_valid())
        self.assertIn('check_in', form.errors.keys())
        self.assertEqual(form.errors['check_in'][0], 'This field is required.')

    def test_checkout_required(self):
        # create form field with blank value
        form = AvailabilityForm({'check_out': ''})
        # check if form valid,error in correct field and correct error produced
        self.assertFalse(form.is_valid())
        self.assertIn('check_out', form.errors.keys())
        self.assertEqual(form.errors['check_out'][0], 'This field is required.')

    def test_only_twofields_are_shown_onform(self):
        # check no other fields have been added to form
        form = AvailabilityForm()
        self.assertEqual(form.Meta.fields, ['check_in', 'check_out'])


@tag('views')
class TestRoombookViews(TestCase):

    def test_availabilityview_get_renders_correct_template(self):
        #  creates an correct instance of RoomType and checks correct template rendered
        item = RoomType.objects.create(type='Single', description='blahblah', price=10, occupancy=1,image_url='', image='')
        response = self.client.get(f'/roombook/book_1/{ item.type}/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'roombook/book_1.html')

    def test_availabilityview_get_renders_correct_template_if_type_wrong(self):
        # creates an incorrect instance of RoomType and checks correct template rendered
        item = RoomType.objects.create(type='wrong', description='blahblah', price=10, occupancy=1,image_url='', image='')
        response = self.client.get(f'/roombook/book_1/{ item.type}/')
        self.assertNotEqual(response.status_code,200)
        self.assertRedirects(response, reverse('home:home'))
        

    def test_availsbility_post_redirects_to_homepage_if_no_available_rooms(self):
        available_rooms = []
        


    def test_bookview_get_renders_correct_template(self):
        # create instance of RoomType
        itemtype = RoomType(type='Single', price=10, occupancy=1) 
        itemtype.save()

        # create instance of Room                                          
        roomnum = Room(room_number=2, type=itemtype)
        roomnum.save()

         # create User instance
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='brian',
                                                   password='dogskin12')

        context = {
                        'user':self.user,
                        'room_number':roomnum,
                        'check_in':'2022-05-01',
                        'check_out':'2022-05-03',
                        'is_active':True,
            }
        response = self.client.get(f'/roombook/book/{context}/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'roombook/book.html')


    def test_bookview_post_creates_booking(self):
        # create instance of RoomType
        itemtype = RoomType(type='Single', price=10, occupancy=1) 
        itemtype.save()

        # create User instance
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='brian',
                                                   password='dogskin12')

        
        # create instance of Room                                          
        roomnum = Room(room_number=2, type=itemtype)
        roomnum.save()

        countbookings = Booking.objects.all().count()
        print(countbookings)
        booking = Booking.objects.create(user=self.user, room_number=roomnum,
                                                        check_in='2022-05-01', check_out='2022-05-03', is_active=True)
        countbookings = Booking.objects.all().count()
        print(countbookings)
        context = {
                # 'user':str(self.request.username),
                'room_number':str(roomnum),
                'check_in':'2022-05-01',
                'check_out':'2022-05-03',
                'is_active':True,

            }
        
            # convert dict to json string
        with open("context.json", "w") as outfile:
            json.dump(context, outfile)

        response = self.client.post(f'/roombook/book/{outfile}/',{
                                                                        'user':self.user,
                                                                        'room_number':roomnum,
                                                                        'check_in':'2022-05-01',
                                                                        'check_out':'2022-05-03',
                                                                        'is_active':True,
                                                            

        })
        print(response.context)
        self.assertEqual(Booking.objects.all().count(),1)





        # # count instances of booking
        # countbookings = Booking.objects.all().count()
        # print(countbookings)
        #  # create instance of RoomType
        # itemtype = RoomType(type='Single', price=10, occupancy=1) 
        # itemtype.save()

        # # create instance of Room                                          
        # roomnum = Room(room_number=2, type=itemtype)
        # roomnum.save()

        #  # create User instance
        # user_model = get_user_model()
        # self.user = user_model.objects.create_user(username='brian',
        #                                            password='dogskin12')

        # context = {
        #                 'user':self.user,
        #                 'room_number':roomnum,
        #                 'check_in':'2022-05-01',
        #                 'check_out':'2022-05-03',
        #                 'is_active':True,
        #     }
        # response = self.client.post(f'/roombook/book/{context}/', {'user':self.user, 'room_number':roomnum,
        #                                                  'check_in':'2022-05-01', 'check_out':'2022-05-03', 'is_active':True})
        # countbookings = Booking.objects.all().count()
        # print(countbookings)
      
        # self.assertRedirects(response, reverse('home:home'))
        # self.assertTemplateUsed(response, 'home/home.html')





    # def test_bookview_redirects_if_user_is_anonymous(self):
        
    #     self.user = AnonymousUser()
    #     response = self.client.post('/roombook/book/{context}')
    #     self.assertTemplateUsed(response, 'roombook/book.html')
    #     # self.assertRedirects(response, reverse('home:home'))





#     def test_availableformview_post_return_home_if_user_not_auth(self):
#         # user_model = get_user_model()
#         # self.user = user_model.objects.create_user(username=' ',
#         #                                            password='hopscotch')
#         self.user = AnonymousUser()
#         item = RoomType.objects.create(type='Single', description='blahblah', price=10, occupancy=1,image_url='', image='')
#         response = self.client.post(f'/book_1/{ item.type}/')
#         self.assertNotEqual(response.status_code, 200)
#         response = self.client.get('')
#         self.assertTemplateUsed(response, 'roombook/home.html')
#         self.assertEqual(response.status_code, 200)


#     def test_type_kwarg_is_correct(self):
#         type = 'wrong'
#         response = self.client.post(f'/book_1/{type}')
#         storage = get_messages(response)
#         for message in storage:
#             print(message)


#             -----------------------------not working------------------------------------------
    
    # def test_type_kwarg_is_correct(self):
    #     type = 'wrong'
    #     types= ['Single', 'Queen', 'Double']
    #     self.assertNotIn(type,types)
    #     response = self.client.post(f'/book_1/{type}/')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/')
        
#-----------------------------------------------------------------------------------------------
   
    # def test_availableformview_post(self):
    #     itemtype = RoomType(type='Single', price=10, occupancy=1) 
    #     itemtype.save()
    #     user_model = get_user_model()
    #     self.user = user_model.objects.create_user(username='brian',
    #                                                password='dogskin12')
    #     roomnum = Room(room_number=2, type=itemtype)
    #     roomnum.save()
    #     booking = Booking(
    #                 user=self.user,
    #                 room_number=roomnum,
    #                 check_in='2022-02-01',
    #                 check_out='2022-02-03',
    #             )
    #     print(len(Booking.objects.all()))
    #     self.book_1_url = reverse('roombook:book_1', args=[itemtype])
    #     response = self.client.post(self.book_1_url,{
    #         'user':self.user,
    #         'room_number':roomnum,
    #         'check_in':'2022-02-02',
    #         'check_out':'2022-02-03'
    #     })
    #     print(len(Booking.objects.all()))
    #     self.assertEquals(response.status_code, 302)







    # def test_check_availability_function_returns_false_if_no_avaikability(self):
    #     #create instance of RoomType
    #     itemtype = RoomType(type='Single', price=10, occupancy=1) 
    #     itemtype.save()
    #     user_model = get_user_model()
    #     self.user = user_model.objects.create_user(username='brian',
    #                                                password='dogskin12')
    #      # create instance of Room                                          
    #     roomnum = Room(room_number=2, type=itemtype)
    #     roomnum.save()
    #     booking = Booking(
    #                 user=self.user,
    #                 room_number=roomnum,
    #                 check_in='2022-02-01',
    #                 check_out='2022-02-03',
    #             )
    #     check_in = '2022-02-01'
    #     check_out = '2022-02-03'
    #     room =2
    #     self.assertEquals(check_availability(room, check_in, check_out), False) 
    
    # def test_booking_being_made(self):
    #     item = RoomType.objects.create(type='Single', description='blahblah', price=10, occupancy=1,image_url='', image='')
    #     response = self.client.post(f'/book_1/{ item.type}')
    #     self.assertTemplateUsed(response, 'roombook/book_1.html')
        
        # # create instance of RoomType
        # itemtype = RoomType(type='Single', price=10, occupancy=1) 
        # itemtype.save()
        # user_model = get_user_model()
        # self.user = user_model.objects.create_user(username='brian',
        #                                            password='dogskin12')
        #  # create instance of Room                                          
        # roomnum = Room(room_number=2, type=itemtype)
        # roomnum.save()
        # booking = Booking(
        #             user=self.user,
        #             room_number=roomnum,
        #             check_in='2022-02-01',
        #             check_out='2022-02-03',
        #         )

        # print(len(Booking.objects.all()))
        # available_rooms = [1,1] 
        # print(itemtype,self.user, roomnum, len(available_rooms))
        # response = self.client.post(f'/book_1/{itemtype}', {'available_rooms':available_rooms, 'user':self.user, 'room_number':roomnum, 'check_in':'2022-02-01', 'check_out':'2022-02-03'})
        # print(len(Booking.objects.all()))
        # self.assertRedirects(response, ' ')

#    def test_can_add_item(self):
#         response = self.client.post('/add', {'name': 'Test Added Item'})
#         self.assertRedirects(response, '/')

#     def test_can_delete_item(self):
#         item = Item.objects.create(name='Test Todo Item')
#         response = self.client.get(f'/delete/{item.id}')
#         self.assertRedirects(response, '/')
#         existing_items = Item.objects.filter(id=item.id)
#         self.assertEqual(len(existing_items), 0)



 
@tag('models')
class TestRoomBookModels(TestCase):

    def test_item_string_method_returns_type_for_roomtype_model(self):
        # create sample row of RoomType table and compare to expected output
        item = RoomType.objects.create(type='Single', description='blahblah', price=10, occupancy=1,image_url='', image='')
        self.assertEqual(str(item), 'Single')

    def test_item_string_method_returns_roomnumber_for_room_model(self):
        itemtype = RoomType(type='Single', price=10, occupancy=1) 
        itemtype.save()
        item = Room.objects.create(room_number=10, type=itemtype)
        self.assertEqual(str(item), '10')

    def test_item_string_method_returns_correct_string_for_booking_model(self):
        # create instance of RoomType
        itemtype = RoomType(type='Single', price=10, occupancy=1) 
        itemtype.save()
        # create User instance
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='brian',
                                                   password='dogskin12')
        # create instance of Room                                          
        roomnum = Room(room_number=2, type=itemtype)
        roomnum.save()
        # create sample Booking table row and compare with expected output
        item = Booking.objects.create(user=self.user, room_number=roomnum , check_in='2022-02-01', check_out='2022-02-03', is_active=True)
        self.assertEqual(str(item),'brian has booked  Room 2 from 2022-02-01 to 2022-02-03')
       


    
        
      


   