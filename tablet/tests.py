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
        url = '/tablet/' + str(room.room_id) + '/quickBook/'
        request = self.factory.post(url)
        User.objects.create_user('user','user@email.com')
        request.POST['id'] = 'user'
        request.POST['date'] = "2017-01-01"
        request.POST['start'] = "09:00"
        request.POST['end'] = "10:00"
        response = quickBook(request)
        print response

    '''
    def testEndEvent(self):

    

    def testQuickBook(self):
    url(r'^$',views.index, name = 'index'),
                url(r'^end_event/$',views.end_event, name = 'end_event'),
                url(r'^bookRoom/$',views.bookRoom, name = 'bookRoom'),
                url(r'^quickBook/$',views.quickBook, name = 'quickBook'),'''