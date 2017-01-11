from django.shortcuts import render
from django.http import HttpResponse
from bksys.models import rooms, bookings
from django.core.exceptions import ObjectDoesNotExist
import time,json
from datetime import datetime, timedelta
from bksys.views import getDate, getTime, set_default_values

room_id = 1

#Check In Option if not checked in 15 min then
def get_events(request):
	if 'start' not in request.POST:
		start = datetime.strptime(getDate(request),"%d-%m-%Y")
		start = start.strftime("%Y-%m-%d")
		end = start
	else:
		start = request.POST['start']
		end = request.POST['end']
	events = bookings.objects.events(room_id,start,end)
	bk_list = [jsonCalendar(bk_instance) for bk_instance in events]
	return bk_list

def index(request):
	bk_for_day = bookings.objects.filter(room_id=room_id,date=time.strftime("%Y-%m-%d"))
	bk_list = [bk_instance.getJSON() for bk_instance in bk_for_day]
	upcoming_events = get_upcoming_events()
	current_event = get_on_going_event()
	if not current_event:
		bk_id = 0
	else:
		bk_id = current_event.booking_ref
	next_event=""
	print upcoming_events
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

def get_bookings(request):
	start_time = request.POST['start']
	end_time = request.POST['end']
	date = request.POST['date']

def bookRoom(request):
	date = getDate(request)
	time = getTime(request)
	scroll_time = datetime.strptime(time,"%H:%M") - timedelta(minutes=60)
	res = {
		"datetime":date + "T"+ time,
		"settings":json.dumps(set_default_values(scroll_time.strftime("%H:%M"),defaultView='agendaDay')),
		"room":rooms.objects.get(room_id=room_id),
		"start_time":getTime(request),
		"date": date,
		'time': time,
		'room_name':rooms.objects.get(room_id=room_id).room_name,
		'bookings':json.dumps(get_events(request)),
	}
	return render(request,"book_room.html",res)
	
def get_on_going_event():
	cTime = time.strftime("%H:%M")
	try:
		ongoing = bookings.objects.get(date=time.strftime("%Y-%m-%d"),room_id=room_id,start_time__lte=cTime,end_time__gte=cTime)
	except ObjectDoesNotExist:
		ongoing = bookings.objects.none()
	return ongoing

def get_upcoming_events():
	cTime = time.strftime("%H:%M")
	upcoming = bookings.objects.filter(date=time.strftime("%Y-%m-%d"),room_id=room_id,start_time__gte=cTime)
	upcoming = upcoming.order_by('start_time')[:3]
	return upcoming

def end_event(request):
	bk_id = request.POST[id]
	bookings.objects.get(booking_ref=bk_id).remove()

def jsonCalendar(booking):
	return dict(
		id = booking.booking_ref,
		title = booking.description,
		isUserCreated = True,
		editable = False,
		start = str(booking.date) + "T" + str(booking.start_time),
		end = str(booking.date) + "T" + str(booking.end_time),
	)
