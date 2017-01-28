from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import json, time
from bksys.models import *
from django.contrib.sessions.middleware import SessionMiddleware
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.common.exceptions import TimeoutException, WebDriverException
from django.conf import settings
from selenium.webdriver.support.ui import Select

class requirementsTest(LiveServerTestCase):
    def setUp(self):
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'browser':'ALL' }
        self.browser = webdriver.Chrome(desired_capabilities=d)
        self.browser.implicitly_wait(3)
        room = rooms.objects.create(room_name="testing",room_size=10,room_location="loc",room_features="feat")
        self.room_id = room.room_id
        self.browser.get(self.live_server_url)

    def insertInput(self,id,value):
        self.browser.find_element_by_id(id).clear()
        self.browser.find_element_by_id(id).send_keys(value)
    
    def insertInputbyName(self,name,value):
        self.browser.find_element_by_name(name).clear()
        self.browser.find_element_by_name(name).send_keys(value)
    
    def tearDown(self):  
        self.browser.quit()
    
    '''
    def testBookRoom(self):
        self.browser.get(self.live_server_url + "/tablet/" + str(self.room_id))
    	users.objects.create_user('user','1yser@user.com')
        self.browser.find_element_by_id('bookRoom').click()
        #Go to next day to avoid clicking on past dates
        self.browser.find_element_by_id('next').click()
        xpath = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[100]/td[2]'
        #Xpath for event coordinates
        self.browser.find_element_by_xpath(xpath).click()
        self.browser.find_element_by_id('book').click()
        time.sleep(1)
        self.insertInput('search','user')
        self.browser.find_element_by_id('confirm').click()
        time.sleep(1)
        self.assertEqual(self.browser.find_element_by_id('modal_roomname').get_attribute('value'),"testing")
        start_time = self.browser.find_element_by_id('modal_stime').get_attribute('value') + ":00"
        end_time = self.browser.find_element_by_id('modal_etime').get_attribute('value') + ":00"
        time.sleep(1)
        self.browser.find_element_by_id('exit_modal').click()
        booking = bookings.objects.all()[0]
        self.assertEqual(booking.room.room_name,"testing")
        self.assertEqual(str(booking.start_time),start_time.strip())
        self.assertEqual(str(booking.end_time),str(end_time))
    

    def testEndEvent(self):
        #Ongoing Booking
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
        self.browser.get(self.live_server_url + "/tablet/" + str(self.room_id))
        self.browser.find_element_by_id('end').click()
        time.sleep(1)
        self.insertInput('search','user')
        self.browser.find_element_by_id('confirm').click()
        time.sleep(1)
        self.assertEqual(len(bookings.objects.all()),0)
        

    '''