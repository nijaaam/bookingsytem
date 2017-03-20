from django.shortcuts import render
from django.http import HttpResponse
from bksys.models import *
from django.core.exceptions import ObjectDoesNotExist
import time,json
from datetime import datetime, timedelta
from bksys.views import set_default_values, getJSONBookings, getJSONRooms

#Check In Option if not checked in 15 min then
room_id = 1

def index(request,id):
	room_id = id
	bk_for_day = bookings.objects.filter(room_id=room_id,date=time.strftime("%Y-%m-%d"))
	bk_list = [getJSONBookings(bk_instance) for bk_instance in bk_for_day]
	upcoming_events = get_upcoming_events()
	start = time.strftime("%H:%M")
	end = time.strftime("%H:%M")
	current_event = bookings.objects.filter(
			date=time.strftime("%Y-%m-%d"),
			end_time__gte = start,
			start_time__lte = end
	).order_by('start_time')
	if current_event:
		current_event = current_event[0]
	if not current_event:
		bk_id = 0
	else:
		bk_id = current_event.booking_ref
	next_event=""
	if not current_event:
		if not upcoming_events:
			next_event = "for the day"
		else:	
			next_event = "until " + upcoming_events[0].start_time.strftime("%H:%M")
	return render(request, "index.html",{
		'room_name':rooms.objects.get(room_id=room_id).room_name,
		'upcoming':upcoming_events,
		'ongoing':current_event,
		'bookings':json.dumps(bk_list),
		'ongoing_bk_id':bk_id,
		'next_event':next_event,
	})	

def quickBook(request,id):
	user = users.objects.getUser(request.POST['id'])
	contact = users.objects.getName(user)
	date = request.POST['date']
	start = request.POST['start']
	end = request.POST['end']
	booking = bookings.objects.newBooking(id,date,start,end,contact,'quickBook',user)
	return render(request,'modal.html',{
	    "booking_id": booking.booking_ref,
	    "room_name": rooms.objects.get_name(id),
        "start_time": start,
	    "end": end,
	})

def showCalendar(request,id):
	date = time.strftime("%d-%m-%Y")
	bk_time = time.strftime("%H:%M")
	scroll_time = datetime.strptime(bk_time,"%H:%M") - timedelta(minutes=60)
	res = {
		"datetime" : date + "T"+ bk_time,
		"settings" : json.dumps(set_default_values(scroll_time.strftime("%H:%M"))),
		'room_name': rooms.objects.get(room_id=id).room_name,
	}
	return render(request,"show_calendar.html",res)

def get_upcoming_events():
	cTime = time.strftime("%H:%M")
	upcoming = bookings.objects.filter(date=time.strftime("%Y-%m-%d"),room_id=room_id,start_time__gte=cTime)
	upcoming = upcoming.order_by('start_time')[:3]
	return upcoming

def end_event(request,id):
	bk_id = request.POST['bk_id']
	bookings.objects.delete(bk_id)
	return HttpResponse(1)
