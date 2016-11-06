from django.conf.urls import  url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
                url(r'^find_rooms/$',views.find_rooms, name = 'find_rooms'),
                url(r'^view_room/([0-9]+)/$',views.view_room, name = 'view_room'),
              ]