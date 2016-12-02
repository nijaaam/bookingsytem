from django.conf.urls import  url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
                url(r'^find_rooms/$',views.find_rooms, name = 'find_rooms'),
                url(r'^view_room/([0-9]+)/$',views.view_room, name = 'view_room'),
                url(r'^book_room/$',views.book_room, name = 'book_room'),
                url(r'^viewBooking/$',views.viewBooking, name = 'viewBooking'),
                url(r'^showWeek/$',views.showWeek, name = 'showWeek'),
                url(r'^prevWeek/$',views.prevWeek, name = 'prevWeek'),
                url(r'^nextWeek/$',views.nextWeek, name = 'nextWeek'),
                url(r'^findBooking/$',views.findBooking, name = 'findBooking'),
                url(r'^updateBooking/$',views.updateBooking, name = 'updateBooking'),
                url(r'^cancelBooking/$',views.cancelBooking, name = 'cancelBooking'),
                url(r'^changeDuration/$',views.changeDuration, name = 'changeDuration'),
                url(r'^getBKDateTime/$',views.getBKDateTime, name = 'getBKDateTime'),
                url(r'^getBookingsDay/$',views.getBookingsDay, name = 'getBookingsDay'),
              ]