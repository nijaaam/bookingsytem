from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from bksys.models import *
import time

class roomsTest(TestCase):
    def setUp(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        self.id = room.room_id

    def tearDown(self):
        rooms.objects.all().delete()

    def test_get_name(self):
        self.assertEqual(rooms.objects.get_name(self.id),"test1")

    def test_retrieve(self):
        room = rooms.objects.get(room_id=self.id)
        self.assertEqual(room.room_name,"test1")

    def test_update_db(self):
        room = rooms.objects.get(room_id=self.id)
        room.room_name = "New name"
        room.save()
        room = rooms.objects.get(room_id=self.id)
        self.assertEqual(room.room_name,"New name")

    def test_delete(self):
        rooms.objects.filter(room_id=self.id).delete()
        self.assertRaises(ObjectDoesNotExist,rooms.objects.get,room_id=1)

class usersTest(TestCase):
    def setUp(self):
        self.passcode = users.objects.create_user('name','email')

    def tearDown(self):
        users.objects.all().delete()

    def test_get_user(self):
        user_id = users.objects.getUser('name')
        user = users.objects.get(id=user_id)
        self.assertEqual(user.email,'email')

    def test_auth(self):
        self.assertEqual(True,users.objects.authenticate('name'))
        self.assertEqual(False,users.objects.authenticate('1name'))
        self.assertEqual(True,users.objects.authenticate(self.passcode))
        self.assertEqual(False,users.objects.authenticate('random'))

    def test_get_name(self):
        user_id = users.objects.getUser('name')
        self.assertEqual('name',users.objects.getName(user_id))

class recurringEventsTest(TestCase):
    def setUp(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        self.id = room.room_id

    def test_new_event(self):
        recurringEvents.objects.newBooking(self.id,"2017-01-01","2017-01-30",2)
        obj = recurringEvents.objects.get(room_id=self.id,recurrence=2,end_date="2017-01-30")
        self.assertEqual(str(obj.start_date),"2017-01-01")

class reservationsTest(TestCase):
    def setUp(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        self.id = room.room_id

    def test_save_retrieve(self):
        obj = reservations.objects.create(room_id=self.id,start_time="2017-01-01 10:00")
        self.assertEqual(reservations.objects.get(id=obj.id).room_id,self.id)

class bookingsTest(TestCase):
    def setUp(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        self.room_id = room.room_id
        users.objects.create_user('name','email')
        self.user_id = users.objects.getUser('name')

    def test_new_booking(self):
        bk = bookings.objects.newBooking(self.room_id,"2017-01-10","10:00","11:00","des","con",self.user_id)
        bk_id = bk.booking_ref
        self.assertEqual(bookings.objects.get(booking_ref=bk_id).room_id,self.room_id)
        self.assertEqual(bookings.objects.get(booking_ref=bk_id).user_id,self.user_id)
        self.assertEqual(bookings.objects.isRecurring(bk_id),False)

    def test_recurring_bookings_and_delete(self):
        booking = bookings.objects.newRecurringBooking(self.room_id,"2017-01-10","10:00","11:00","con","des",2,"29-01-2017",self.user_id)
        #should create three bookings and recurr object
        self.assertEqual(len(bookings.objects.all()),3)
        self.assertEqual(len(recurringEvents.objects.all()),1)
        self.assertEqual(bookings.objects.isRecurring(booking.booking_ref),True)
        bookings.objects.deleteAllRecurring(booking.booking_ref)
        self.assertEqual(len(bookings.objects.all()),0)

    def test_get_attributes(self):
        bk = bookings.objects.newBooking(self.room_id,"2017-01-10","10:00","11:00","con","des",self.user_id)
        self.assertEqual(bookings.objects.description(bk.booking_ref),"des")
        self.assertEqual(bookings.objects.contact(bk.booking_ref),"con")
        self.assertEqual(bookings.objects.formatDate(bk.booking_ref),"10-01-2017 10:00:00 - 11:00:00")

    def test_delete(self):
        bk = bookings.objects.newBooking(self.room_id,"2017-01-10","10:00","11:00","con","des",self.user_id)
        id = bk.booking_ref
        bookings.objects.delete(id)
        self.assertRaises(ObjectDoesNotExist,bookings.objects.get,booking_ref=id)

    def test_ongoing_events(self):
        date = time.strftime("%Y-%m-%d")
        start = datetime.now().strftime('%H:%M')
        end = datetime.now() + timedelta(minutes=15)
        end = end.strftime("%H:%M")
        self.assertEqual(len(bookings.objects.getOngoingEvents(date,start,start)),0)
        bk = bookings.objects.newBooking(self.room_id,date,start,end,"des","con",self.user_id)
        self.assertEqual(len(bookings.objects.getOngoingEvents(date,start,start)),1)

    def test_user_bookings(self):
        bk = bookings.objects.newBooking(self.room_id,"2017-01-10","10:00","11:00","des","con",self.user_id)
        self.assertEqual(len(bookings.objects.getUserBookings(self.user_id)),1)

    def test_remove_expired_entries(self):
        date = time.strftime("%Y-%m-%d")
        prev_date = datetime.now() - timedelta(days=1)
        prev_date.strftime("%Y-%m-%d")
        start = datetime.now().strftime('%H:%M')
        end = datetime.now() + timedelta(minutes=15)
        end = end.strftime("%H:%M")
        bk = bookings.objects.newBooking(self.room_id,date,start,end,"des","con",self.user_id)
        bk = bookings.objects.newBooking(self.room_id,prev_date,start,end,"des","con",self.user_id)
        self.assertEqual(len(bookings.objects.all()),2)
        bookings.objects.removeStaleBookings()
        self.assertEqual(len(bookings.objects.all()),1)
