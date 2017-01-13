from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from bksys.models import *

class RoomsTest(TestCase):
    def setUp(self):
        room = rooms(
            room_id = 1,
            room_name = "Room Test 1", 
            room_size = 11, 
            room_location = "Location",
            room_features =  "Features",
        )
        room.save()

    def test_save_and_retreive(self):
        room = rooms.objects.get(room_id=1)
        self.assertEqual(room.room_id,1)
        self.assertEqual(room.room_name,"Room Test 1")
        self.assertEqual(room.room_size,11)
        self.assertEqual(room.room_location,"Location")
        self.assertEqual(room.room_features,"Features")

    def testGetJSON(self):
        room = rooms.objects.get(room_id=1)
        json = room.getJSON()
        self.assertEqual(json['room_id'],1)
        self.assertEqual(json['room_name'],"Room Test 1")
        self.assertEqual(json['room_size'],11)
        self.assertEqual(json['room_location'],"Location")
        self.assertEqual(json['room_features'],"Features")

    def test_update_db(self):
        rooms.objects.filter(room_id=1).update(room_name="New name")
        room = rooms.objects.get(room_id=1)
        self.assertEqual(room.room_name,"New name")

    def test_delete(self):
        rooms.objects.filter(room_id=1).delete()
        self.assertRaises(ObjectDoesNotExist,rooms.objects.get,room_id=1)
    

class BookingsTest(TestCase):
    def setUp(self):
        room = rooms(
            room_id = 1,
            room_name = "Room Test 1", 
            room_size = 11, 
            room_location = "Location",
            room_features =  "Features",
        )
        room.save()
        booking = bookings(
            booking_ref=1,
            room_id = 1,
            date = "2017-01-13",
            start_time = "09:15:00",
            end_time = "10:15:00",
            contact = "contact",
            description = "description",
        )
        booking.save()

    def test_save_and_retreive(self):
        booking = bookings.objects.get(booking_ref=1)
        self.assertEqual(booking.booking_ref,1)
        self.assertEqual(booking.room_id,1)
        self.assertEqual(str(booking.date),"2017-01-13")
        self.assertEqual(str(booking.start_time),"09:15:00")
        self.assertEqual(str(booking.end_time),"10:15:00")
        self.assertEqual(booking.contact,"contact")
        self.assertEqual(booking.description,"description")
        
    def testGetJSON(self):
        booking = bookings.objects.get(booking_ref=1)
        json = booking.getJSON()
        self.assertEqual(json['booking_ref'],1)
        self.assertEqual(json['room_id'],1)
        self.assertEqual(str(json['date']),"2017-01-13")
        self.assertEqual(str(json['start_time']),"09:15:00")
        self.assertEqual(str(json['end_time']),"10:15:00")
        self.assertEqual(json['contact'],"contact")
        self.assertEqual(json['description'],"description")

    def test_update_db(self):
        bookings.objects.filter(booking_ref=1).update(contact="New contact")
        booking = bookings.objects.get(booking_ref=1)
        self.assertEqual(booking.contact,"New contact")

    def test_delete(self):
        bookings.objects.get(booking_ref=1).delete()
        self.assertRaises(ObjectDoesNotExist,bookings.objects.get,booking_ref=1)    

class RoomsManagerTest(TestCase):
    def setUp(self):
        room = rooms(
            room_id = 1,
            room_name = "Room Test 1", 
            room_size = 11, 
            room_location = "Location",
            room_features =  "Features",
        )
        room.save()

    def test_get_name(self):
        self.assertEqual(rooms.objects.get_name(1),"Room Test 1")

    def test_get_queryset(self):
        self.assertQuerysetEqual(rooms.objects.get_queryset(),[repr(r) for r in rooms.objects.all()])

class BookingsManagerTest(TestCase):
    def setUp(self):
        room = rooms(
            room_id = 1,
            room_name = "Room Test 1", 
            room_size = 11, 
            room_location = "Location",
            room_features =  "Features",
        )
        room.save()

    def testMethods(self):
        bookings.objects.newBooking(1,"2017-01-13","09:15:00","10:15:00","contact","description")
        self.assertEqual(bookings.objects.description(1),"description")
        self.assertEqual(bookings.objects.contact(1),"contact")
        self.assertEqual(bookings.objects.formatDate(1),"13-01-2017 09:15:00 - 10:15:00")
        self.assertQuerysetEqual(bookings.objects.get_queryset(),[repr(r) for r in bookings.objects.all()])
        ongoingevent = bookings.objects.getOngoingEvents("2017-01-13","09:30","09:30")
        self.assertQuerysetEqual(bookings.objects.get_queryset(),[repr(r) for r in ongoingevent])
        bookings.objects.delete(1)
        self.assertRaises(ObjectDoesNotExist,bookings.objects.get,booking_ref=1)
        #Weekly Repeat from Jan 13 - Feb 25 - 7 Bookings
        bookings.objects.newRecurringBooking(1,"2017-01-13","09:15:00","10:15:00","contact","description",2,"25-02-2017")
        print bookings.objects.all()