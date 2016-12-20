from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from .models import rooms, bookings
from tests import globalTestMethods
import time

class RequirementsTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		rooms(room_name="Room Test",room_size=5,room_location="TEST",room_features="TEST FEatu").save()
		self.browser.get("http://localhost:8081")
		self.obj = globalTestMethods(self.browser)

	def tearDown(self):  
		self.browser.quit()

	def testBookRoom(self):
		obj = self.obj
		browser = self.browser
		obj.book_room()
		booking_id = bookings.objects.last().booking_ref
		booking =  bookings.objects.get(booking_ref=booking_id)
		self.assertEqual(booking.contact,"contact")
		self.assertEqual(booking.description,"description")


		obj.viewBooking(str(booking_id))
		obj.updateInput('contact',"updated contact")
		obj.updateInput('description',"updated description")
		browser.find_element_by_id('update').click()
		time.sleep(2)
		booking_id = bookings.objects.last().booking_ref
		booking =  bookings.objects.get(booking_ref=booking_id)
		self.assertEqual(booking.contact,"updated contact")
		self.assertEqual(booking.description,"updated description")
		browser.implicitly_wait(3)

		obj.viewBooking(str(booking_id))
		browser.find_element_by_id('cancelBooking').click()
		time.sleep(3)
		browser.find_element_by_id('cancelBooking2').click()
		time.sleep(3)
		self.assertEqual(None,bookings.objects.last())
