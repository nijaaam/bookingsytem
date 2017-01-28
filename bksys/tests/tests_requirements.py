from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import json, time
from bksys.models import *
from django.contrib.sessions.middleware import SessionMiddleware
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from django.conf import settings
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import Select

class requirementsTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        rooms.objects.create(room_name="testing",room_size=10,room_location="loc",room_features="feat")
        self.browser.get(self.live_server_url)

    def insertInput(self,id,value):
        self.browser.find_element_by_id(id).clear()
        self.browser.find_element_by_id(id).send_keys(value)
    
    def insertInputbyName(self,name,value):
        self.browser.find_element_by_name(name).clear()
        self.browser.find_element_by_name(name).send_keys(value)
    
    def tearDown(self):  
        self.browser.quit()

    def testBookRoom(self):
    	#user need to signup first
    	self.browser.find_element_by_xpath("//a[contains(text(), 'Sign Up')]").click()
    	self.browser.implicitly_wait(3)
    	self.insertInput('id_name','user')
    	self.insertInput('id_email','user@user.com')
    	self.browser.find_element_by_xpath("//button[contains(text(), 'Sign Up')]").click()
    	self.browser.implicitly_wait(3)
    	self.browser.find_element_by_xpath("//a[contains(text(), 'Back')]").click()
    	self.browser.find_element_by_xpath("//button[contains(text(), 'Book')]").click()
    	self.insertInput('contact','contact')
    	self.insertInput('description','description')
    	select = Select(self.browser.find_element_by_id('recurring'))
    	select.select_by_visible_text('Never')
    	self.insertInput('search','user')
    	self.browser.find_element_by_xpath("//button[contains(text(), 'Book')]").click()
    	self.browser.implicitly_wait(3)
    	self.browser.find_element_by_id('modal_roomname').get_attribute('value')
    	
