from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from tablet.views import *

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
    	print url
    	response = self.client.get(url)
    	self.assertEqual(response.status_code,200)
    	self.assertTemplateUsed(response,'book_room.html')

    '''
    def testEndEvent(self):

    

    def testQuickBook(self):
    url(r'^$',views.index, name = 'index'),
				url(r'^end_event/$',views.end_event, name = 'end_event'),
				url(r'^bookRoom/$',views.bookRoom, name = 'bookRoom'),
				url(r'^quickBook/$',views.quickBook, name = 'quickBook'),'''