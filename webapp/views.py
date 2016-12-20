from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime, timedelta, date
from .models import rooms,bookings, reservations
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
		cDate = time.strftime("%d-%m-%Y")
	res = generateResponse(cDate,cTime,request)
	return render(request,'home.html',res)

def validateTime(cDate,cTime,request):
	if cDate < time.strftime("%d-%m-%Y"):
		cTime = time.strftime("%H:%M")
		cDate = time.strftime("%d-%m-%Y")
	if cTime < time.strftime("%H:%M"):
		if cDate == time.strftime("%d-%m-%Y"):
			cTime = time.strftime("%H:%M")
	request.session['bk_date'] = cDate
	request.session['bk_time'] = cTime
	return cDate,cTime

def find_rooms(request):
	bk_date = request.POST['bk_date']
	bk_time = request.POST['bk_time'] 	 	
	res = generateResponse(bk_date,bk_time,request)
	return render(request,'home.html',res)

def getRoomsBookings(request):
	start = request.POST['start']
	end = request.POST['end']
	all_rooms = rooms.objects.all()
	rooms_json = [rm_instance.getJSON() for rm_instance in all_rooms]
	room_bookings = []
	for rm_instance in all_rooms:
		booking_list = bookings.objects.filter(room_id=rm_instance.room_id,date__range=[start,end]) 
		room_bookings.append([bk_instance.getJSON() for bk_instance in booking_list])
	results = {
    	'bookings': json.dumps(room_bookings)
	}
	return HttpResponse(json.dumps(results), content_type="application/json")
	

def checkIfExpired(id):
	reserve = reservations.objects.get(room_id=id)
	expires =  reserve.expiry.replace(tzinfo=None)
	elapsed_time = datetime.now() - expires
	if (elapsed_time - timedelta(minutes = 2)).total_seconds() > 0:
		return 1
	else:
		return 0

def queryDB(date,time):
	end = datetime.strptime(time,"%H:%M") + timedelta(minutes=15)
	end = end.strftime("%H:%M")
	query_date = datetime.strptime(date,"%d-%m-%Y").strftime("%Y-%m-%d")
	booked_room_ids = bookings.objects.filter(date = query_date,start_time__lte=time,end_time__gte=end).values_list('room_id',flat=True)
	avaliable_rooms = rooms.objects.exclude(room_id__in = booked_room_ids)
	reserved_rooms = []
	'''
	for room in avaliable_rooms:
		try:
			reserved_room = reservations.objects.get(room_id=room.room_id)
			if checkIfExpired(room.room_id):
				reservations.objects.get(room_id=room.room_id).delete()
				reserved_rooms.append(room)				
		except ObjectDoesNotExist:
			reserved_rooms.append(room)
	avaliable_rooms = reserved_rooms
	'''
	all_rooms = rooms.objects.all()
	rooms_json = [rm_instance.getJSON() for rm_instance in all_rooms]
	room_bookings = []
	for rm_instance in all_rooms:
		booking_list = bookings.objects.filter(room_id=rm_instance.room_id,date=datetime.strptime(date,"%d-%m-%Y").strftime("%Y-%m-%d"))
		room_bookings.append([bk_instance.getJSON() for bk_instance in booking_list])
	return avaliable_rooms,room_bookings,rooms_json

def generateResponse(date,time,request):
	(date,time) = validateTime(date,time,request)
	scroll_time = datetime.strptime(time,"%H:%M") - timedelta(minutes=60)
	(avaliable_rooms,room_bookings,rooms_json) = queryDB(date,time)
	response = {
    	'scroll_time': scroll_time.strftime("%H:%M"),
    	'rooms': json.dumps(rooms_json), 
    	'bookings': json.dumps(room_bookings),
    	'bk_date':date,
    	'bk_time':time,
    	'query_results':avaliable_rooms,
    	'current_date':datetime.strptime(date,"%d-%m-%Y").strftime("%Y-%m-%d") }
	return response
    
def view_room(request,id):
	#reservations(room_id=id).save()
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
		"event_id": str(room_id) + "," + str(entry.booking_ref),
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
		return render(request,'showResult.html',{
		"room_name": room.room_name,
		"room_size": room.room_size,
		"room_location": room.room_location,
		"room_features": room.room_features,
		"contact": booking.contact,
		"description": booking.description,
		"start":booking.start_time.strftime("%H:%M"),
		"end":booking.end_time.strftime("%H:%M"),
		"date":booking.date.strftime("%d-%m-%Y"),
		"booking_id":booking_id,
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
		"date": str(booking.date.strftime("%d-%m-%Y")) + " " + str(booking.start_time) + " - " + str(booking.end_time)
	})

def cancelBooking(request):
	booking_id = request.POST['booking_id']
	bookings.objects.filter(booking_ref=booking_id).delete()
	return HttpResponse("Booking Canceled")

def getBookings(request):
	start = request.POST['start']
	end = request.POST['end']
	room_name = request.POST['room_name']
	room = rooms.objects.get(room_name=room_name)
	start = datetime.strptime(start,"%d-%m-%Y").strftime("%Y-%m-%d")
	end = datetime.strptime(end,"%d-%m-%Y").strftime("%Y-%m-%d")
	booking_list = bookings.objects.filter(room_id=room.room_id,date__range=[start,end]) 
	results = [bk_instance.getJSON() for bk_instance in booking_list]
	return HttpResponse(json.dumps(results), content_type="application/json")
