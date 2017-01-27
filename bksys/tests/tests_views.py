from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from django.contrib.sessions.middleware import SessionMiddleware
from tablet.views import *
from bksys.models import * 
from bksys.views import * 

class viewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def add_session(self,request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        return request
    '''
    def testIndex(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        rooms.objects.create(room_name="test2",room_size=10,room_features="feat",room_location="loc")
        users.objects.create_user('name','email')
        user_id = users.objects.getUser('name')
        bookings.objects.newBooking(
            room.room_id,
            time.strftime("%Y-%m-%d"),
            time.strftime("%H:%M"),
            time.strftime("%H:%M"),
            "contact",
            "description",
            user_id,
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        scroll_time = datetime.now() - timedelta(minutes=60)
        scroll_time = scroll_time.strftime("%H:%M")
        self.assertEqual(scroll_time,response.context['scroll_time'])
        form = response.context['form']
        self.assertEqual(form.is_valid(),True)
        if form.is_valid():
            self.assertEqual(str(form.cleaned_data['date']),time.strftime("%Y-%m-%d"))
            self.assertEqual(form.cleaned_data['time'].strftime("%H:%M"),time.strftime("%H:%M"))
        avaliable_rooms = response.context['query_results']
        #Only Room 1 should be in list since Room 2 is booked
        self.assertEqual(len(avaliable_rooms),1)
        rooms_json = json.loads(response.context['rooms'])
        self.assertEqual(len(rooms_json),1)
        bookings_json = json.loads(response.context['bookings'])
        self.assertEqual(len(bookings_json),0)
        self.assertEqual(response.context['current_date'],time.strftime("%Y-%m-%d"))

    def testViewRoom(self):
        room = rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        response = self.client.post('/view_room/',{'room_id':room.room_id})
        self.assertEqual(response.context['room'],rooms.objects.get(room_id=room.room_id))
        self.assertEqual(response.context['start_time'],time.strftime("%H:%M"))
        self.assertEqual(response.context['date'],time.strftime("%d-%m-%Y"))
        scroll_time = datetime.strptime(time.strftime("%H:%M"),"%H:%M") - timedelta(minutes=60)
        settings = json.dumps(set_default_values(scroll_time.strftime("%H:%M")))
        self.assertEqual(response.context['settings'],settings)
    
    def checkContext(self,response,name,value):
        self.assertEqual(response.context[name],value)

    def testBookRoom(self):
        room = rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        session = self.client.session
        session['bk_rm_id'] = room.room_id
        session.save()
        response = self.client.post('/book_room/',{'id':'name',"recurring":"0","contact":"contact","description":"description","start":"10:00","end":"11:00","date":time.strftime("%Y-%m-%d")})
        self.checkContext(response,'start_time',"10:00")
        self.checkContext(response,'end',"11:00")
        self.checkContext(response,'booking_id',bookings.objects.last().booking_ref)
        self.checkContext(response,'event_id', str(room.room_id) + "," + str(bookings.objects.last().booking_ref))

    def testViewBooking(self):
        response = self.client.get('/viewBooking/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'viewBooking.html')

    def testFindBooking(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        bk = bookings.objects.newBooking(room.room_id,"2017-01-10","10:00","11:00","des","con",user_id)
        id = bk.booking_ref
        response = self.client.post('/findBooking/',{'booking_id':id})
        self.checkContext(response,'room',room)
        self.checkContext(response,'booking',bk)
        response = self.client.post('/findBooking/',{'booking_id':999})
        self.assertContains(response,"<span class = 'help-block' style ='color:#a94442'>Booking not found for 999</span>")
        
    def testUpdateBooking(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        bk = bookings.objects.newBooking(room.room_id,"2017-01-10","10:00","11:00","des","con",user_id)
        id = bk.booking_ref
        response = self.client.post('/updateBooking/',{'booking_id':id,'description':'new_description'})
        booking = bookings.objects.get(booking_ref=id)
        self.assertEqual(booking.description,"new_description")

    def testCancelBooking(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        bk = bookings.objects.newBooking(room.room_id,"2017-01-10","10:00","11:00","des","con",user_id)
        id = bk.booking_ref
        response = self.client.post('/cancelBooking/',{'id':id,'deleteAll':'false'})
        self.assertRaises(ObjectDoesNotExist,bookings.objects.get,booking_ref=id)
        #cancel recurring bookings
        booking = bookings.objects.newRecurringBooking(room.room_id,"2017-01-10","10:00","11:00","con","des",2,"29-01-2017",user_id)
        #should create three bookings and recurr object
        self.assertEqual(len(bookings.objects.all()),3)
        self.assertEqual(len(recurringEvents.objects.all()),1)
        self.assertEqual(bookings.objects.isRecurring(booking.booking_ref),True)
        response = self.client.post('/cancelBooking/',{'id':booking.booking_ref,'deleteAll':'true'})
        self.assertEqual(len(bookings.objects.all()),0)

    def testGetBookings(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        room_name = room.room_name
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        bk = bookings.objects.newBooking(room.room_id,"2017-01-10","10:00","11:00","des","con",user_id)
        id = bk.booking_ref
        request = self.factory.post('/getBookings/')
        request.POST['room_name'] = room_name
        request.POST['start'] =  "09-01-2017"
        request.POST['end'] =  "11-01-2017"
        response = getBookings(request)
        bookings_json = json.loads(response.content)
        self.assertEqual(len(bookings_json),1)
    
    def testGetRoomsBookings(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        room_name = room.room_name
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        bookings.objects.newBooking(room.room_id,"2017-01-10","10:00","11:00","des","con",user_id)
        bookings.objects.newBooking(room.room_id,"2017-01-11","10:00","11:00","des","con",user_id)
        bookings.objects.newBooking(room.room_id,"2017-01-12","10:00","11:00","des","con",user_id)
        request = self.factory.post('/getRoomsBookings')
        request.POST['start'] =  "2017-01-09"
        request.POST['end'] =  "2017-01-11"
        request = self.add_session(request)
        request.session['bk_time'] = time.strftime('%H:%M')
        response = getRoomsBookings(request)
        bookings_json = json.loads(response.content)
        self.assertEqual(len(bookings_json),2)
        self.assertEqual(bookings_json[0]['room_id'],room.room_id)
        self.assertEqual(bookings_json[1]['room_id'],room.room_id)

    '''
    def testCheckIfRecurring(self):
        request = self.factory.post('/checkIfRecurring')
        response = checkIfRecurring(request)
        print response

    '''
    def testSignup(self):
        request = self.factory.post('/signup')
        response = signup(request)
        print response

    def testAutocomplete(self):
        request = self.factory.post('/autocomplete')
        response = autocomplete(request)
        print response

    def testValidateID(self):
        request = self.factory.post('/validateID')
        response = validateID(request)
        print response

    def testGetUserBookings(self):
        request = self.factory.post('/getUserBookings')
        response = getUserBookings(request)
        print response
        
            
       
        '''
        
'''

    def testGetRoomBookings(self):
        response = client.post('/getRoomsBookings/',{
            'start':"2017-01-01",
            'end':"2017-01-31",
        })
        self.assertEqual(response.status_code,200)
        bookings_json = response.json()
        self.assertEqual(len(bookings_json),1)
        self.assertEqual(bookings_json[0]['description'],"description")
        self.assertEqual(bookings_json[0]['contact'],"contact")
        #New Booking to test if response has the new booking
        booking = bookings(
            room_id    = 3,
            date       = time.strftime("%Y-%m-%d"),
            start_time = time.strftime("%H:%M"),
            end_time=time.strftime("%H:%M"),
            contact="contact 2",
            description="description 2"
        )
        booking.save()
        response = client.post('/getRoomsBookings/',{
            'start':"2017-01-01",
            'end':"2017-01-31",
        })
        self.assertEqual(response.status_code,200)
        bookings_json = response.json()
        self.assertEqual(len(bookings_json),2)
        self.assertEqual(bookings_json[0]['description'],"description")
        self.assertEqual(bookings_json[0]['contact'],"contact")
        self.assertEqual(bookings_json[1]['description'],"description 2")
        self.assertEqual(bookings_json[1]['contact'],"contact 2")      
    
'''