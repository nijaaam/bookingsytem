from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime, timedelta, date
from .models import rooms,bookings, reservations
from django.core.exceptions import ObjectDoesNotExist
import time, json
from .forms import DateTimeForm


def index(request):
    form = processForm(request)
    bk_date = getDate(request)
    bk_date = datetime.strptime(bk_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    bk_start_time = getTime(request)
    bk_end_time = datetime.strptime(bk_start_time,"%H:%M") + timedelta(minutes=15)
    scroll_time = datetime.strptime(bk_start_time,"%H:%M") - timedelta(minutes=60)
    avaliable_rooms = avaliableRooms(bk_date,bk_start_time,bk_end_time)
    rooms_json = [rm_instance.getJSON() for rm_instance in avaliable_rooms]
    room_bookings = []
    for room in avaliable_rooms:
        booking_list = bookings.objects.filter(room_id=room.room_id,date=bk_date)
        for booking in booking_list:
            room_bookings.append(booking.getJSON())
    response = {
        'scroll_time': scroll_time.strftime("%H:%M"),
        'rooms': json.dumps(rooms_json), 
        'bookings': json.dumps(room_bookings),
        'query_results': avaliable_rooms,
        'current_date': time.strftime("%Y-%m-%d"),
        'table_height': getTableHeight(len(avaliable_rooms)),
        'form': form,
    }
    return render(request,'home.html',response)

def getRoomsBookings(request):
    start = request.POST['start']
    end = request.POST['end']
    avaliable_rooms = avaliableRooms(start,getTime(request),getTime(request))
    rooms_json = [rm_instance.getJSON() for rm_instance in avaliable_rooms]
    bookings_list = []
    for room in avaliable_rooms:
        booking_list = bookings.objects.filter(room_id=room.room_id,date__range=[start,end])
        for booking in booking_list:
            bookings_list.append(booking.getJSON())
    return HttpResponse(json.dumps(bookings_list), content_type="application/json")

def avaliableRooms(date,start,end):
    ongoingevents = bookings.objects.getOngoingEvents(date,start,end).values_list('room_id',flat=True)
    avaliable_rooms = rooms.objects.exclude(room_id__in = ongoingevents)
    return avaliable_rooms

def checkIfExpired(id):
    reserve = reservations.objects.get(room_id=id)
    expires =  reserve.expiry.replace(tzinfo=None)
    elapsed_time = datetime.now() - expires
    if (elapsed_time - timedelta(minutes = 2)).total_seconds() > 0:
        return 1
    else:
        return 0
    
def getDate(request):
    if 'bk_date' in request.session:
        return request.session['bk_date']
    else:
        return time.strftime("%d-%m-%Y")

def getTime(request):
    if 'bk_time' in request.session:
        return request.session['bk_time']
    else:
        return time.strftime("%H:%M")

def findBooking(request):
    booking_id = request.POST['booking_id']
    try:
        booking = bookings.objects.get(booking_ref=booking_id)
        if datetime.strptime(str(booking.date)+str(booking.end_time),"%Y-%m-%d%H:%M:%S") < datetime.now():
            bookings.objects.delete(booking_id)
            error_msg = "Booking not found for " + booking_id
            html = "<span class = 'help-block' style ='color:#a94442'>" + error_msg + "</span>"
            return HttpResponse(html)
        room = rooms.objects.get(room_id=booking.room_id)
        start = booking.start_time.strftime("%H:%M")
        end = booking.end_time.strftime("%H:%M")
        date = booking.date.strftime("%d-%m-%Y")
        scroll_time = datetime.strptime(start,"%H:%M") - timedelta(minutes=60)
        return render(request,'showResult.html',{
            "room":room,
            "booking":booking,
            "datetime":date +"T"+ start,
            "start":start,
            "end":end,
            "date":date,
            "settings": json.dumps(set_default_values(scroll_time.strftime("%H:%M"))),
        })
    except ObjectDoesNotExist:
        error_msg = "Booking not found for " + booking_id
        html = "<span class = 'help-block' style ='color:#a94442'>" + error_msg + "</span>"
        return HttpResponse(html)

def if_values_are_set(f):
    def test(request):
        if 'room_id' in request.POST:
            return f(request)
        else:
            return redirect('/')

    return test

@if_values_are_set
def view_room(request):
    #reservations(room_id=id).save()
    id = request.POST['room_id']
    request.session['bk_rm_id'] = id
    query = rooms.objects.get(room_id=id)
    date = getDate(request)
    time = getTime(request)
    start_time = date + "T" + time
    scroll_time = datetime.strptime(time,"%H:%M") - timedelta(minutes=60)
    res = {
        "datetime":date +"T"+ time,
        "settings":json.dumps(set_default_values(scroll_time.strftime("%H:%M"))),
        "room":query,
        "start_time":getTime(request),
        "date":getDate(request)
    }
    return render(request,'room_details.html',res)

def book_room(request):
    recurring = request.POST.getlist('recurring')[0]
    contact         = request.POST['contact']
    description     = request.POST['description']
    start = request.POST['start']
    end =  request.POST['end']
    date =  request.POST['date']
    room_id = request.session['bk_rm_id']    
    if recurring == "0":
        entry = bookings.objects.newBooking(room_id,date,start,end,contact,description)
    else:
        entry = bookings.objects.newRecurringBooking(room_id,date,start,end,contact,description,recurring,request.POST['recurr_end'])
    room_name = rooms.objects.get_name(room_id)
    return render(request,'modal.html',{
        "booking_id":entry.booking_ref,
        "event_id": str(room_id) + "," + str(entry.booking_ref),
        "room_name": room_name,
        "start_time":start,
        "end":end,
    })

def viewBooking(request):
    return render(request,'viewBooking.html',{})


def updateBooking(request):
    booking_id = request.POST['booking_id']
    for key in request.POST:
        value = request.POST[key]
        if value != " " and key != 'booking_id':
            if key == 'description':
                bookings.objects.filter(booking_ref=booking_id).update(description=value)
            if key == 'contact':
                bookings.objects.filter(booking_ref=booking_id).update(contact=value)
            if key == 'date' or key == 'start' or key == 'end':
                date = request.POST['date']
                start = request.POST['start']
                end = request.POST['end']
                bookings.objects.filter(booking_ref=booking_id).update(date=date,start_time=start,end_time=end)
    booking = bookings.objects.get(booking_ref=booking_id)
    return render(request,"updatedBKModal.html",{
        "booking_id": booking_id,
        "room_name": rooms.objects.get_name(booking.room_id),
        "description": bookings.objects.description(booking_id),
        "contact": bookings.objects.contact(booking_id),
        "date": bookings.objects.formatDate(booking_id), 
    })

def cancelBooking(request):
    if request.POST['deleteAll'] == "true":
        bookings.objects.deleteAllRecurring(request.POST['id'])
        return HttpResponse("Bookings Canceled")
    else:
        bookings.objects.delete(request.POST['id'])
        return HttpResponse("Booking Canceled")
   

def getCalendarEventJson(booking):
    return dict(
        id = booking.booking_ref,
        title = booking.description,
        start = str(booking.date) + "T" + str(booking.start_time),
        end = str(booking.date) + "T" + str(booking.end_time),
        isUserCreated = True,
        editable = False,
    )

def getBookings(request):
    start = request.POST['start']
    end = request.POST['end']
    room_name = request.POST['room_name']
    room = rooms.objects.get(room_name=room_name)
    start = datetime.strptime(start,"%d-%m-%Y").strftime("%Y-%m-%d")
    end = datetime.strptime(end,"%d-%m-%Y").strftime("%Y-%m-%d")
    booking_list = bookings.objects.filter(room_id=room.room_id,date__range=[start,end]) 
    results = [getCalendarEventJson(bk_instance) for bk_instance in booking_list]
    #results = [bk_instance.getJSON() for bk_instance in booking_list]
    return HttpResponse(json.dumps(results), content_type="application/json")

def set_default_values(scrollTime):
    return dict(
        header = dict(
            left = '',
            center = '',
            right = '',
        ),
        firstDay       = 1,
        longPressDelay = 200,
        minTime        = "08:00:00",
        height         = '500',
        margin         = '0 auto',
        defaultDate  = 'datetime',
        defaultView  = 'agendaWeek',
        maxTime      = "19:00:00",
        allDaySlot   = False,
        editable     = True,
        eventLimit   = True,
        eventOverlap = False,
        slotDuration = '00:05:00',
        nowIndicator = True,
        scrollTime   = scrollTime,
    )

def processForm(request):
    if not request.POST:
        form = DateTimeForm({'date':getDate(request),'time':getTime(request)})
    else:
        form = DateTimeForm(request.POST)
        if form.is_valid():
            form_date = form.cleaned_data['date']
            form_time = form.cleaned_data['time']
            request.session['bk_date'] = form_date.strftime("%d-%m-%Y")
            request.session['bk_time'] = form_time.strftime("%H:%M")
            form = DateTimeForm(initial={'date': form_date.strftime("%d-%m-%Y"), 'time':form_time.strftime("%H:%M")})
    return form

def getTableHeight(rowCount):
    if rowCount == 0:
        return 79
    elif rowCount < 4:
        return rowCount*67 + 39
    else:
        return 250

def checkIfRecurring(request):
    if (bookings.objects.isRecurring(request.POST["id"])):
        return HttpResponse(1)
    return HttpResponse(0)
    