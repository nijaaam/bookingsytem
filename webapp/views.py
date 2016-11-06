from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from .models import rooms,bookings
import time

def index(request):
	res = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id NOT IN (SELECT room_id FROM webapp_bookings WHERE date = '2016-11-01' AND start_time > '12:50' AND start_time < '13:00')")
	print (len(list(res)))
	cDate = time.strftime("%d-%m-%Y")
	cTime = time.strftime("%H:%M")
	return render_to_response('home.html', {'query_results': res, 'cDate':cDate, 'cTime':cTime})