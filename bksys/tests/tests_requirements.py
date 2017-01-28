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
    
    '''
    def testSignUp(self):
        self.browser.find_element_by_xpath("//a[contains(text(), 'Sign Up')]").click()
        self.browser.implicitly_wait(3)
        self.insertInput('id_name','user')
        self.insertInput('id_email','user@user.com')
        self.browser.find_element_by_xpath("//button[contains(text(), 'Sign Up')]").click()
        self.browser.implicitly_wait(3)
        self.browser.find_element_by_xpath("//a[contains(text(), 'Back')]").click()
        
    def testBookRoom(self):
    	users.objects.create_user('user','yser@user.com') #User
        self.browser.find_element_by_xpath("//button[contains(text(), 'Book')]").click()
        #Enter values
        self.insertInput('contact','contact')
        self.insertInput('description','description')
        select = Select(self.browser.find_element_by_id('recurring'))
        select.select_by_visible_text('Never')
        self.insertInput('search','user')
        self.browser.execute_script("$('#search').typeahead('close');")
        #Submit
        self.browser.find_element_by_xpath("//button[contains(text(), 'Book')]").click()
        self.browser.implicitly_wait(3)
        #Assert Values
        self.assertEqual(self.browser.find_element_by_id('modal_roomname').get_attribute('value'),"testing")
        start_time = self.browser.find_element_by_id('modal_stime').get_attribute('value')
        end_time = self.browser.find_element_by_id('modal_etime').get_attribute('value')
        time.sleep(1)
        self.browser.find_element_by_id('exit_modal1').click()
        booking = bookings.objects.all()[0]
        self.assertEqual(booking.room.room_name,"testing")
        self.assertEqual(str(booking.start_time),start_time.strip())
        self.assertEqual(str(booking.end_time),str(end_time))
    '''

    def testUpdateBooking(self):
        room = rooms.objects.create(room_name="test1",room_size=10,room_features="feat",room_location="loc")
        users.objects.create_user('name','email@a.com')
        user_id = users.objects.getUser('name')
        start = datetime.now() + timedelta(minutes=5)
        end = datetime.now() + timedelta(minutes=20)
        bk = bookings.objects.newBooking(
            room.room_id,
            time.strftime("%Y-%m-%d"),
            start.strftime('%H:%M'),
            end.strftime('%H:%M'),
            "contact",
            "description",
            user_id,
        )
        view_booking_path = '//*[@id="bs-example-navbar-collapse-1"]/ul/li[2]/a'
        self.browser.find_element_by_xpath(view_booking_path).click()
        self.insertInput('search','name')
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="authUser"]/div/div/span[2]/button').click()
        
        #Click the first booking
        self.browser.find_element_by_xpath('//*[@id="userBookings"]/div/div[2]/table/tbody/tr[1]/td[5]/div/button').click()
        time.sleep(1)
        #update contact and description
        self.insertInput('contact','update_c')
        self.insertInput('description','update_d')
        #open calendar
        self.browser.find_element_by_xpath('//*[@id="openCal"]').click()
        time.sleep(1)
        #move event
        self.browser.execute_script('testMoveEvent()')
        time.sleep(9)


'''

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