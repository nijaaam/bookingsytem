from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.core.urlresolvers import resolve
from django.test import LiveServerTestCase
from django.test import TestCase
from webapp.views import index, viewBooking
import time
from datetime import datetime, timedelta, date

'''
class HomePageTest(TestCase):

    def testHomePage(self):
        found = resolve('/')  
        self.assertEqual(found.func, index)  

class HomePageLiveTest(LiveServerTestCase):

	def setUp(self):  
		self.browser = webdriver.Firefox()
		self.browser.get("http://localhost:8000")

	def tearDown(self):  
		self.browser.quit()

	def testDateTime(self):	
		browser = self.browser
		bk_date = browser.find_element_by_id('bk_date').get_attribute('value')
		bk_time = browser.find_element_by_id('bk_time').get_attribute('value')
		self.assertEqual(time.strftime("%H:%M"),bk_time)
		self.assertEqual(time.strftime("%d-%m-%Y"),bk_date)
		#Testing Sessions
		bk_date = datetime.strptime(bk_date,"%d-%m-%Y") + timedelta(days=2)
		bk_time = datetime.strptime(bk_time,"%H:%M") + timedelta(minutes=15)
		bk_date = bk_date.strftime("%d-%m-%Y")
		bk_time = bk_time.strftime("%H:%M")
		#Added Time
		browser.find_element_by_id('bk_date').clear()
		browser.find_element_by_id('bk_time').clear()
		browser.find_element_by_id('bk_date').send_keys(bk_date)
		browser.find_element_by_id('bk_time').send_keys(bk_time)
		#Inserted Input
		browser.find_element_by_id('find_room_btn').click()
		#Trigger Find Rooms
		self.assertEqual(bk_date,browser.find_element_by_id('bk_date').get_attribute('value'))
		self.assertEqual(bk_time,browser.find_element_by_id('bk_time').get_attribute('value'))

class ViewBookingLiveTest(LiveServerTestCase):

	def setUp(self):  
		self.browser = webdriver.Firefox()
		self.browser.get("http://localhost:8000/")

	def tearDown(self):  
		self.browser.quit()

	def testUrlResolve(self):
		found = resolve('/viewBooking/')
		self.assertEqual(found.func,viewBooking)

class BookRoomLiveTest(LiveServerTestCase):
	def setUp(self):  
		self.browser = webdriver.Firefox()
		self.browser.get("http://localhost:8000/")
		self.browser.get("http://localhost:8000/view_room/1/")

	def tearDown(self):  
		self.browser.quit()

	def testIfBookedRoomsAppearsOnTable(self):
		browser = self.browser
		browser.implicitly_wait(3)
		table = browser.find_elements_by_tag_name('tbody')
		rows = browser.find_elements_by_tag_name('tr')
		name = ""
		for row in rows:
			col = row.find_elements_by_tag_name('td')	
			if len(col) > 0:
				name = col[0].text
				browser.implicitly_wait(3)
				col[4].find_elements_by_tag_name('form')[0].find_elements_by_tag_name('button')[0].click()
				break
		browser.find_element_by_id('contact').send_keys("contact")
		browser.find_element_by_id('description').send_keys("description")
		browser.implicitly_wait(3)
		browser.find_element_by_id('book_button').click()
		browser.implicitly_wait(1)
		self.browser.get("http://localhost:8000/")
		table = browser.find_elements_by_tag_name('tbody')
		rows = browser.find_elements_by_tag_name('tr')
		for row in rows:
			col = row.find_elements_by_tag_name('td')	
			if len(col) > 0:
				self.assertNotEqual(col[0].text,name)
				break
		
	
	

'''