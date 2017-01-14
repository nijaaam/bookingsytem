from django.test import TestCase, Client
from django.urls import reverse
from bksys.models import rooms, bookings
from datetime import datetime, timedelta
import time, json 

client = Client()

class bksysViewTest(TestCase):
    def setUp(self):
        room = rooms(
            room_id = 2,
            room_name = "Room Test 1", 
            room_size = 11, 
            room_location = "Location",
            room_features =  "Features",
        )
        room.save()
        room = rooms(
            room_id = 3,
            room_name = "Room Test 2", 
            room_size = 11, 
            room_location = "Location 2",
            room_features =  "Features 2",
        )
        room.save()
        booking = bookings(
            room_id    = 2,
            date       ="2017-01-14",
            start_time ="08:00",
            end_time="09:00",
            contact="contact",
            description="description"
        )
        booking.save()
         

    def testIndex(self):
        response = self.client.get('/')
        scroll_time = datetime.now() - timedelta(minutes=60)
        scroll_time = scroll_time.strftime("%H:%M")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scroll_time,response.context['scroll_time'])
        self.assertEqual(time.strftime("%d-%m-%Y"),response.context['bk_date'])
        self.assertEqual(time.strftime("%H:%M"),response.context['bk_time'])
        self.assertEqual(time.strftime("%Y-%m-%d"),response.context['current_date'])
        form = response.context['form']
        self.assertEqual(form.is_valid(),True)
        if form.is_valid():
            self.assertEqual(str(form.cleaned_data['date']),time.strftime("%Y-%m-%d"))
            self.assertEqual(form.cleaned_data['time'].strftime("%H:%M"),time.strftime("%H:%M"))
        avaliable_rooms = response.context['query_results']
        #Only Room 1 should be in list since Room 2 is booked
        self.assertEqual(len(avaliable_rooms),1)
        self.assertEqual(avaliable_rooms[0].room_name,"Room Test 2")
        if len(avaliable_rooms) == 0:
            self.assertEqual(79,response.context['table_height'])
        elif len(avaliable_rooms) < 4:
            self.assertEqual(len(avaliable_rooms)*67 + 39,response.context['table_height'])
        rooms_json = json.loads(response.context['rooms'])
        #There should be two rooms
        self.assertEqual(rooms_json[0]['room_name'],"Room Test 1")
        self.assertEqual(rooms_json[1]['room_name'],"Room Test 2")
        bookings_json = json.loads(response.context['bookings'])
        #Room 2 should be booked
        self.assertEqual(bookings_json[0][0]['room_id'],2)

    
