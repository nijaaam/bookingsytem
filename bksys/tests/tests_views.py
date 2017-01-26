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