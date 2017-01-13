from django.test import TestCase, Client
from django.urls import reverse
from bksys.models import rooms
from datetime import datetime, timedelta
import time, json 

client = Client()

class bksysViewTest(TestCase):
    def setUp(self):
        room = rooms(
            room_id = 1,
            room_name = "Room Test 1", 
            room_size = 11, 
            room_location = "Location",
            room_features =  "Features",
        )
        room.save()

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
        if len(avaliable_rooms) == 0:
            self.assertEqual(79,response.context['table_height'])
        elif len(avaliable_rooms) < 4:
            self.assertEqual(len(avaliable_rooms)*67 + 39,response.context['table_height'])
        rooms_json = json.loads(response.context['rooms'])
        bookings_json = json.loads(response.context['bookings'])
    
