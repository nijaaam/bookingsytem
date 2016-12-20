from django.test import TestCase
from .models import rooms, bookings
'''
class RoomsBookingsTest(TestCase):
	def testDB(self):
		room = rooms(1,"Room Test 1", 11, "TEST LOC", "TEST FEA")
		room.save()
		room = rooms.objects.get(room_id=1)
		self.assertEqual(room.room_name,"Room Test 1")



'''