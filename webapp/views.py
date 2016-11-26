from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime, timedelta, date
from .models import rooms,bookings
import time

def index(request):
	try:
		cDate = request.session['bk_date']
		cTime = request.session['bk_time']  
	except KeyError:
		cTime = time.strftime("%H:%M")
		cDate = time.strftime("%d-%m-%Y")
	res = queryDB(cDate,cTime,request)
	return render(request,'home.html',res)

def find_rooms(request):
	cTime = time.strftime("%H:%M")
	bk_date = request.POST['bk_date']
	bk_time = request.POST['bk_time']
	if time < cTime:
		bk_time = cTime
	res = queryDB(bk_date,bk_time,request)
	return render(request,'home.html',res)

def viewBooking(request):
	return render(request,'viewBooking.html',{})

def showWeek(request):
	dt = datetime.now()
	dt_str = dt.strftime("%Y-%m-%d")
	start = dt - timedelta(days = dt.weekday())
	end = start + timedelta(days=6)
	start1	 = str(start.strftime("%d-%m-%y"))
	start = str(start.strftime("%Y-%m-%d"))
	request.session['weekNo'] = start
	end = str(end.strftime("%Y-%m-%d"))
	res = rooms.objects.raw("SELECT * FROM webapp_bookings WHERE room_id = %s AND date > %s AND date < %s",[request.session['bk_rm_id'],start,end])
	return render_to_response('events_table.html',{"query_results":res,"weekNo":start1})

def getBookingsforWeek(request,x):
	dt = request.session['weekNo']
	dt = datetime.strptime(dt,"%Y-%m-%d")
	if x == "-":
	    start = dt - timedelta(days = 7)
	elif x == "+":
		start = dt + timedelta(days = 7)
	end = start + timedelta(days=6)
	start1	 = str(start.strftime("%d-%m-%y"))
	start = str(start.strftime("%Y-%m-%d"))
	request.session['weekNo'] = start
	end = str(end.strftime("%Y-%m-%d"))
	#res1 = bookings.objects.filter(room_id=request.session['bk_rm_id']).filter(date__end__lte = 0).filter(date__start__gte = 0) 
	res = rooms.objects.raw("SELECT * FROM webapp_bookings WHERE room_id = %s AND date > %s AND date < %s",[request.session['bk_rm_id'],start,end])
	#print list(res1),list(res)
	return start1,res

def prevWeek(request):
	(weekNo,res) = getBookingsforWeek(request,"-")
	return render_to_response('events_table.html',{"query_results":res,"weekNo":weekNo})

def nextWeek(request):
	(weekNo,res) = getBookingsforWeek(request,"+")
	return render_to_response('events_table.html',{"query_results":res,"weekNo":weekNo})

def queryDB(date,time,request):
	request.session['bk_date'] = date
	request.session['bk_time'] = time
	print date, time
	res = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id NOT IN (SELECT room_id FROM webapp_bookings WHERE date = '2016-11-08' AND start_time < '19:12' AND end_time < '19:27')")
	obj = {'query_results': res, 'bk_date':date, 'bk_time':time}
	return obj

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
	elif radio[0] == "userDuration":
		return request.POST['durValue'] 

def convertMinutes(request):
	minutes = getMinutes(request)
	hours = minutes[0] + minutes[1]
	hours = int(hours)
	minutes1 = minutes[3]+ minutes[4]
	min = int(minutes1) + 60*hours
	return minutes,min

def findBooking(request):
	res = rooms.objects.raw("SELECT * FROM webapp_bookings,webapp_rooms WHERE booking_ref = %s AND webapp_bookings.room_id = webapp_rooms.room_id;",[request.POST['booking_id']]);
	start = list(res)[0].start_time.strftime("%H:%M")
	end = list(res)[0].end_time.strftime("%H:%M")
	duration = "end - start"
	start_arr = start.split(":")
	hours = int(end.split(":")[0]) - int(start.split(":")[0])
	minutes = int(end.split(":")[1]) - int(start.split(":")[1])
	if minutes < 0:
		hours = hours - 1
		minutes = 60 + minutes
	elif minutes == 0:
		minutes = "00"
	duration = str(hours) + ":" + str(minutes)
	return render(request,'showResult.html',{"query_results":res,"duration":duration})

def book_room(request):
	contact	     = request.POST['contact']
	description	 = request.POST['description']
	date = request.session['bk_date']
	start_time = request.session['bk_time']
	start_time = datetime.strptime(start_time,"%H:%M")
	(minutes,min) = convertMinutes(request)
	calc_time = start_time + timedelta(minutes=min)
	end_time = str(calc_time.hour) + ":" + str(calc_time.minute)
	room_id = request.session['bk_rm_id']
	entry = bookings(room_id= room_id,start_time=start_time,end_time=end_time,contact=contact,description=description)
	entry.save()
	queryRoom = rooms.objects.filter(room_id=room_id)
	room_name = list(queryRoom)[0].room_name
	print room_name
	return render(request,'modal.html',{
		"booking_id":entry.booking_ref,
		"room_name": room_name,
		"start_time":start_time.strftime("%H:%M"),
		"duration":minutes,
		})

def view_room(request,id):
	request.session['bk_rm_id'] = id
	query = rooms.objects.raw("SELECT * FROM webapp_rooms WHERE room_id = %s",[id])
	res = {"room_details":query}
	return render(request,'room_details.html',res)

def updateBooking(request):
	booking_id = request.POST['booking_id']
	res = bookings.objects.filter(booking_ref=booking_id)
	description = request.POST['description']
	contact = request.POST['contact']
	duration =""
	room_name = " KJLKJ KL"
	if description != list(res)[0].description:
		bookings.objects.filter(booking_ref=booking_id).update(description=description)
	if contact != list(res)[0].contact:
		bookings.objects.filter(booking_ref=booking_id).update(contact=contact)
	return render(request,"updatedBKModal.html",{
		"booking_id": booking_id,
		"room_name": room_name,
		"description": description,
		"contact": contact,
		"duration": duration,
		})
	

def cancelBooking(request):
	booking_id = request.POST['booking_id']
	bookings.objects.filter(booking_ref=booking_id).delete()
	return HttpResponse("Booking Canceled")