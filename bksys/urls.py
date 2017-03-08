from django.conf.urls import  url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
                url(r'^view_room/$',views.view_room, name = 'view_room'),
                url(r'^book_room/$',views.book_room, name = 'book_room'),
                url(r'^viewBooking/$',views.viewBooking, name = 'viewBooking'),
                url(r'^findBooking/$',views.findBooking, name = 'findBooking'),
                url(r'^updateBooking/$',views.updateBooking, name = 'updateBooking'),
                url(r'^cancelBooking/$',views.cancelBooking, name = 'cancelBooking'),
                url(r'^getBookings/$',views.getBookings, name = 'getBookings'),
                url(r'^getRoomsBookings/$',views.getRoomsBookings, name = 'getRoomsBookings'),
                url(r'^checkIfRecurring/$',views.checkIfRecurring, name = 'checkIfRecurring'),
                url(r'^signup/$',views.signup, name = 'signup'),
                url(r'^view_room/autocomplete/$',views.autocomplete, name = 'autocomplete'),
                url(r'^validateID/$',views.validateID, name = 'validateID'),
                url(r'^getUserBookings/$',views.getUserBookings, name = 'getUserBookings'),
              ]