from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from tablet.views import *
from bksys.models import * 

class viewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def testIndex(self):
        room = rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        url = '/tablet/' + str(room.room_id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')
        self.assertContains(response,'<span style="font-size: 170%;" class="pull-left">name</span>')

    def testBookRoom(self):
        room = rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        url = '/tablet/' + str(room.room_id) + '/bookRoom/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'book_room.html')
        self.assertEqual(response.context['room_name'],room.room_name)

    def testQuickBook(self):
    	room = rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        users.objects.create_user('user','user@email.com')
        url = '/tablet/' + str(room.room_id) + '/bookRoom/quickBook/'
        response = self.client.post(url,{'id':'user','date':'2017-01-01','start':'09:00','end':'10:00'})
        self.assertEqual(len(bookings.objects.all()),1)
        self.assertEqual(response.context['room_name'],"name")
        self.assertEqual(response.context['start_time'],"09:00")
        self.assertEqual(response.context['end'],"10:00")
    
    def testEndEvent(self):
        room = rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        users.objects.create_user('user','user@email.com')
        user_id = users.objects.getUser('user')
        bk = bookings.objects.newBooking(
            room.room_id,
            time.strftime("%Y-%m-%d"),
            time.strftime("%H:%M"),
            time.strftime("%H:%M"),
            "contact",
            "description",
            user_id,
        )
        response = self.client.post('end_event',{'bk_id':bk.booking_ref})
        self.assertEqual(len(bookings.objects.all()),1)
