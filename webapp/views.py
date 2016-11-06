from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from .models import rooms,bookings
import time

def index(request):
	cDate = time.strftime("%d-%m-%Y")
	cTime = time.strftime("%H:%M")
	res = queryDB(cDate,cTime)
	return render_to_response('home.html',res)

def queryDB(date,time):
	res = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id NOT IN (SELECT room_id FROM webapp_bookings WHERE date = '2016-11-01' AND start_time > '12:50' AND start_time < '13:00')")
	obj = {'query_results': res, 'date':date, 'time':time}
	return obj

@csrf_exempt
def find_rooms(request):
	date = request.POST['date']
	time = request.POST['start_time']
	res = queryDB(date,time)
	return render_to_response('home.html',res)

def queryRoom(id):
	res = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id = %s",[id])
	return res

def view_room(request,id):
	return render_to_response('room_details.html',{"room_details":queryRoom(id)})
	