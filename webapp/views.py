from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime, timedelta, date
from .models import rooms,bookings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import time
import json
from django.core.serializers.json import DjangoJSONEncoder


def index(request):
	try:
		cDate = request.session['bk_date']
		cTime = request.session['bk_time']
	except KeyError:
		cTime = time.strftime("%H:%M")
		cDate = time.strftime("%Y-%m-%d")
	res = queryDB(cDate,cTime,request)
	return render(request,'home.html',res)

def find_rooms(request):
	bk_date = request.POST['bk_date']
	bk_time = request.POST['bk_time'] 	 	
	res = queryDB(bk_date,bk_time,request)
	return render(request,'home.html',res)

def view_room(request,id):
	request.session['bk_rm_id'] = id
	query = rooms.objects.filter(room_id=id)
	start_time = request.session['bk_date'] + "T" + request.session['bk_time']
	res = {"room_details":query,"start_time":request.session['bk_time'],"date":request.session['bk_date']}
	return render(request,'room_details.html',res)

def book_room(request):
	contact	     = request.POST['contact']
	description	 = request.POST['description']
	start = request.POST['start']
	end =  request.POST['end']
	date =  request.POST['date']
	room_id = request.session['bk_rm_id']
	entry = bookings(room_id= room_id,date=date,start_time=start,end_time=end,contact=contact,description=description)
	entry.save()
	queryRoom = rooms.objects.filter(room_id=room_id)
	room_name = list(queryRoom)[0].room_name
	return render(request,'modal.html',{
		"booking_id":entry.booking_ref,
		"room_name": room_name,
		"start_time":start,
		"end":end,
	})

def viewBooking(request):
	return render(request,'viewBooking.html',{})

def findBooking(request):
	booking_id = request.POST['booking_id']
	try:
		booking = bookings.objects.get(booking_ref=booking_id)
		room = rooms.objects.get(room_id=booking.room_id)
		start = booking.start_time.strftime("%H:%M")
		end = booking.end_time.strftime("%H:%M")
		return render(request,'showResult.html',{
		"room_name": room.room_name,
		"room_size": room.room_size,
		"room_location": room.room_location,
		"room_features": room.room_features,
		"contact": booking.contact,
		"description": booking.description,
		})
	except ObjectDoesNotExist:
		error_msg = "Booking not found for " + booking_id
		html = "<span class = 'help-block' style ='color:#a94442'>" + error_msg + "</span>"
		return HttpResponse(html)

def updateBooking(request):
	booking_id = request.POST['booking_id']
	res = bookings.objects.filter(booking_ref=booking_id)
	description = request.POST['description']
	contact = request.POST['contact']
	booking = bookings.objects.get(booking_ref=booking_id)
	room = rooms.objects.get(room_id=booking.room_id)
	room_name = room.room_name
	if description != list(res)[0].description:
		bookings.objects.filter(booking_ref=booking_id).update(description=description)
	if contact != list(res)[0].contact:
		bookings.objects.filter(booking_ref=booking_id).update(contact=contact)
	return render(request,"updatedBKModal.html",{
		"booking_id": booking_id,
		"room_name": room_name,
		"description": description,
		"contact": contact,
	})

def changeDuration(request):
	booking_id = request.POST['booking_id']
	return render(request,"changeDuration.html",{"room_avail":"X"})

def cancelBooking(request):
	booking_id = request.POST['booking_id']
	bookings.objects.filter(booking_ref=booking_id).delete()
	return HttpResponse("Booking Canceled")

def getBKDateTime(request):
	booking = bookings.objects.get(booking_ref = request.GET['booking_id'])
	return JsonResponse({'start_time':booking.start_time,'end_time':booking.end_time,'date':booking.date})

def getBookingsforWeek(request,x):
	dt = request.session['weekNo']
	room_id = request.session['bk_rm_id']
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
	res = bookings.objects.filter(room_id=room_id,date__range=[start,end]) 
	return start1,res

def calculateDifference(now,start):
	start = start.strftime("%H:%M")
	start = datetime.strptime(start,"%H:%M")
	now = datetime.strptime(now,"%H:%M")
	result = str(start - now)
	result = datetime.strptime(result,"%H:%M:%S")
	return result.strftime("%H:%M")


def validateTime(cDate,cTime,request):
	if cDate < time.strftime("%Y-%m-%d"):
			cTime = time.strftime("%H:%M")
			cDate = time.strftime("%Y-%m-%d")
	if cTime < time.strftime("%H:%M"):
			cTime = time.strftime("%H:%M")
	request.session['bk_date'] = cDate
	request.session['bk_time'] = cTime
	return cDate,cTime

def queryDB(date,time,request):
	(date,time) = validateTime(date,time,request)
	date = datetime.strptime(date,"%d-%m-%Y").strftime("%Y-%m-%d")
	end = datetime.strptime(time,"%H:%M") + timedelta(minutes=15)
	end = end.strftime("%H:%M")
	booked_room_ids = bookings.objects.filter(date=date,start_time__lte=time,end_time__gte=end).values_list('room_id',flat=True)
	avaliable_rooms = rooms.objects.exclude(room_id__in = booked_room_ids)
	date = datetime.strptime(date,"%Y-%m-%d").strftime("%d-%m-%Y")
	obj = {'query_results': avaliable_rooms, 'bk_date':date, 'bk_time':time}
	return obj

def getBookings(request):
	start = request.POST['start']
	end = request.POST['end']
	room_name = request.POST['room_name']
	room = rooms.objects.get(room_name=room_name)
	booking_list = bookings.objects.filter(room_id=room.room_id,date__range=[start,end]) 
	results = [bk_instance.getJSON() for bk_instance in booking_list]
	return HttpResponse(json.dumps(results), content_type="application/json")
