from django.shortcuts import render
from django.http import HttpResponse
from bksys.models import rooms, bookings
import time, datetime, json

def index(request):
	bk_for_day = bookings.objects.filter(room_id=26,date=time.strftime("%Y-%m-%d"))
	bk_list = [bk_instance.getJSON() for bk_instance in bk_for_day]
	print bk_list
	return render(request, "index.html",{
		'room_name':"DD",
		'up_events':get_upcoming_events(),
		'ongoing':get_on_going_events(),
		'bookings':json.dumps(bk_list),
	})	

def get_on_going_events():
	cTime = time.strftime("%H:%M")
	ongoing = bookings.objects.filter(date=time.strftime("%Y-%m-%d"),room_id=26,start_time__lte=cTime,end_time__gte=cTime)
	print ongoing
	return ongoing

def get_upcoming_events():
	cTime = time.strftime("%H:%M")
	upcoming = bookings.objects.filter(date=time.strftime("%Y-%m-%d"),room_id=26	,start_time__gte=cTime)
	return upcoming

def end_event(request):
	bk_id = request.POST[id]
	bookings.objects.get(booking_ref=bk_id).remove()


