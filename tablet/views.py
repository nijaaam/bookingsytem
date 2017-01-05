from django.shortcuts import render
from django.http import HttpResponse
from bksys.models import rooms, bookings
from django.core.exceptions import ObjectDoesNotExist
import time, datetime, json

def index(request):
	bk_for_day = bookings.objects.filter(room_id=24,date=time.strftime("%Y-%m-%d"))
	bk_list = [bk_instance.getJSON() for bk_instance in bk_for_day]
	upcoming_events = get_upcoming_events()
	current_event = get_on_going_event()
	if not current_event:
		bk_id = 0
	else:
		bk_id = current_event.booking_ref
	return render(request, "index.html",{
		'room_name':"DD",
		'upcoming':upcoming_events,
		'ongoing':current_event,
		'bookings':json.dumps(bk_list),
		'ongoing_bk_id':bk_id
	})	

def get_on_going_event():
	cTime = time.strftime("%H:%M")
	try:
		ongoing = bookings.objects.get(date=time.strftime("%Y-%m-%d"),room_id=24,start_time__lte=cTime,end_time__gte=cTime)
	except ObjectDoesNotExist:
		ongoing = bookings.objects.none()
	return ongoing

def get_upcoming_events():
	cTime = time.strftime("%H:%M")
	upcoming = bookings.objects.filter(date=time.strftime("%Y-%m-%d"),room_id=24,start_time__gte=cTime)
	upcoming = upcoming.order_by('start_time')[:3]
	return upcoming

def end_event(request):
	bk_id = request.POST[id]
	bookings.objects.get(booking_ref=bk_id).remove()


