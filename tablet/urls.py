from django.conf.urls import  url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
				url(r'^end_event/$',views.end_event, name = 'end_event'),
				url(r'^bookRoom/$',views.bookRoom, name = 'bookRoom'),
				url(r'^bookRoom/quickBook/$',views.quickBook, name = 'quickBook'),
              ]