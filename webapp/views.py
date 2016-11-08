from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import rooms,bookings
import time

def index(request):
	cDate = time.strftime("%d-%m-%Y")
	cTime = time.strftime("%H:%M")
	res = queryDB(cDate,cTime,request)
	return render_to_response('home.html',res)

def queryDB(date,time,request):
	request.session['bk_date'] = date
	request.session['bk_time'] = time
	res = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id NOT IN (SELECT room_id FROM webapp_bookings WHERE date = '2016-11-01' AND start_time > '12:50' AND start_time < '13:00')")
	obj = {'query_results': res, 'date':date, 'time':time}
	return obj

@csrf_exempt
def find_rooms(request):
	date = request.POST['date']
	time = request.POST['start_time']
	res = queryDB(date,time,request)
	return render_to_response('home.html',res)

def getMinutes(request):
	radio = request.POST.getlist("duration_radio")
	if radio[0] == "quarter":
	    return "00:15"
	elif radio[0] == "half":
		return "00:30"
	elif radio[0] == "threequarter":
		return "00:45"
	elif radio[0] == "onehour":
		return "01:00"
	elif radio[0] == "otherDuration":
		return request.POST['durValue'] 

@csrf_exempt
def book_room(request):
	contact	     = request.POST['contact']
	description	 = request.POST['description']
	minutes = getMinutes(request)
	start_time = request.session['bk_time']
	start_time = datetime.strptime(start_time,"%H:%M")
	date = request.session['bk_date']
	min = 10
	hours = minutes[0] + minutes[1]
	hours = int(hours)
	minutes = minutes[3]+ minutes[4]
	min = int(minutes) + 60*hours
	calc_time = start_time + timedelta(minutes=min)
	end_time = str(calc_time.hour) + ":" + str(calc_time.minute)
	entry = bookings(booking_ref=1,room_id=1,start_time=start_time,end_time=end_time,contact="X",description="Y")
	entry.save()


def queryRoom(id):
	res = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id = %s",[id])
	return res

def view_room(request,id):
	return render_to_response('room_details.html',{"room_details":queryRoom(id)})
	