from django.db import models
from datetime import date, datetime, timedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY, SU, MO, TU, WE, TH, FR, SA


class BookingsQueryset(models.query.QuerySet):
    def get_booking(self,id):
        return self.get(booking_ref=id)
    
    def get_description(self,id):
        return self.get_booking(id).description

    def get_contact(self,id):
        return self.get_booking(id).contact    

    def formatDate(self,id):
        booking = self.get_booking(id)
        return str(booking.date.strftime("%d-%m-%Y")) + " " + str(booking.start_time) + " - " + str(booking.end_time)

    def delete(self,id):
        self.get_booking(id).delete()

    def ongoingevents(self,date,start,end):
        bookings_for_day = self.filter(date=date)
        ongoingevents = bookings_for_day.filter(end_time__gte = start,start_time__lte = end)
        return ongoingevents

class BookingsManager(models.Manager):
    def newBooking(self,room_id,date,start,end,contact,description):
        booking = self.create(room_id=room_id,date=date,start_time=start,end_time=end,contact=contact,description=description)
        return booking

    def newRecurringBooking(self,room_id,date,start,end,contact,description,type,recur_end):
        recur_end = datetime.strptime(recur_end,"%d-%m-%Y")
        start_date = datetime.strptime(date,"%Y-%m-%d")
        dates = []
        frequency = 1
        if type == 1:
        	frequency = 1
        elif type == 2:
        	frequency = 7
        elif type == 3:
        	frequency = 14
        while True:
        	start_date = start_date + timedelta(days=frequency)
        	if start_date > recur_end:
        		break;
        	else:
        		dates.append(start_date)
        print dates
        recur_end = recur_end.strftime("%Y-%m-%d")
        r_booking = recurringBookings.objects.newBooking(room_id,date,recur_end,type)
        booking = self.create(room_id=room_id,date=date,start_time=start,end_time=end,contact=contact,description=description,recurrence_id=r_booking.id)
        return booking

    def getOngoingEvents(self,date,start,end):
        return self.get_queryset().ongoingevents(date,start,end)

    def get_queryset(self):
        return BookingsQueryset(self.model, using=self._db)

    def delete(self,id):
        self.get_queryset().delete(id)

    def description(self,id):
        return self.get_queryset().get_description(id)

    def contact(self,id):
        return self.get_queryset().get_contact(id)

    def formatDate(self,id):
        return self.get_queryset.formatDate(id)

class recurringBookingsManager(models.Manager):
    def newBooking(self,rm_id,start,end,recur_type):
        return self.create(room_id=rm_id,start_date=start,end_date=end,recurence=recur_type)

class RoomsQueryset(models.query.QuerySet):
    def get_name(self,id):
        query = self.get(room_id=id)
        return query.room_name

class RoomsManager(models.Manager):
    def get_queryset(self):
        return RoomsQueryset(self.model, using=self._db)

    def get_name(self,id):
        return self.get_queryset().get_name(id)

class rooms(models.Model):
    room_id         = models.AutoField(primary_key=True)
    room_name       = models.CharField(max_length=60, null = False)
    room_size       = models.IntegerField(null = False)
    room_location   = models.TextField(null = False)
    room_features   = models.TextField(null = False)
    in_use             = models.BooleanField(default=True)

    objects = RoomsManager()
    def getJSON(self):
        return dict(
            room_id = self.room_id,
            room_name = self.room_name,
            room_size = self.room_size,
            room_location = self.room_location,
            room_features = self.room_features,
        )

class reservations(models.Model):
    reservations_id = models.AutoField(primary_key = True, null = False)
    room               = models.ForeignKey(rooms,  on_delete=models.CASCADE, null = False)
    expiry             = models.DateTimeField(auto_now_add=True)

class recurringBookings(models.Model):
    id = models.AutoField(primary_key = True, null = False)
    room = models.ForeignKey(rooms,  on_delete=models.CASCADE, null=False)
    start_date = models.DateField(null = False)
    end_date = models.DateField(null = False)
    recurrence_options = (
        ('1','Daily'),
        ('2','Weekly'),
        ('3',"Biweekly"),
    )
    recurence = models.CharField(max_length=10,choices=recurrence_options)
    objects = recurringBookingsManager()

class bookings(models.Model):
    booking_ref = models.AutoField(primary_key=True)
    room        = models.ForeignKey(rooms,  on_delete=models.CASCADE, null = False)
    date        = models.DateField(null = False)
    start_time  = models.TimeField(null = False)
    end_time    = models.TimeField(null = False)
    contact     = models.CharField(max_length=60, null = False)
    description = models.CharField(max_length=60, null = False)
    recurrence  = models.ForeignKey(recurringBookings,  on_delete=models.CASCADE, null = False)
    objects = BookingsManager()

    def getJSON(self):
        return dict(
            booking_ref = self.booking_ref,
            room_id = self.room_id,
            date = str(self.date),
            start_time = str(self.start_time),
            end_time = str(self.end_time),
            contact = self.contact,
            description = self.description
        )

