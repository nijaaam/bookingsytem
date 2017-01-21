from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class UserManager(models.Manager):
    def create_user(self, name, email):
        now = timezone.now()
        passcode = User.objects.make_random_password(length=6)
        passcode = make_password(passcode)
        user = self.create(name=name,email=email,passcode=passcode)
        return user

class recurringEventsManager(models.Manager):
    def newBooking(self,rm_id,start,end,recur_type):
        return self.create(room_id=rm_id,start_date=start,end_date=end,recurrence=recur_type)

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

    def deleteAllRecurring(self,id):
        for booking in self.filter(recurrence_id=id):
            booking.delete()

    def delete(self,id):
        self.get_booking(id).delete()

    def ongoingevents(self,date,start,end):
        bookings_for_day = self.filter(date=date)
        ongoingevents = bookings_for_day.filter(end_time__gte = start,start_time__lte = end)
        return ongoingevents

    def isRecurring(self,id):
        booking = self.get_booking(id)
        if booking.recurrence == None:
            return 0
        else:
            return 1

class BookingsManager(models.Manager):
    def newBooking(self,room_id,date,start,end,contact,description):
        booking = self.create(room_id=room_id,date=date,start_time=start,end_time=end,contact=contact,description=description)
        return booking

    def getInterval(self,value):
        if value == "1":
            return 1
        elif value == "2":
            return 7
        elif value == "3":
            return 14

    def deleteAllRecurring(self,id):
        recurrence = self.get_queryset().get_booking(id).recurrence
        self.get_queryset().deleteAllRecurring(recurrence.id)

    def newRecurringBooking(self,room_id,date,start,end,contact,description,type,recur_end):
        recur_end = datetime.strptime(recur_end,"%d-%m-%Y")
        start_date = datetime.strptime(date,"%Y-%m-%d")
        dates = []
        weekend = set([5, 6])
        while True:
            start_date = start_date + timedelta(days=self.getInterval(type))
            if start_date > recur_end:
                break;
            elif start_date.weekday() in weekend:
                print start_date
            else:
                dates.append(start_date)
        recur_end = recur_end.strftime("%Y-%m-%d")
        r_booking = recurringEvents.objects.newBooking(room_id,date,recur_end,type)
        booking = self.create(room_id=room_id,date=date,start_time=start,end_time=end,contact=contact,description=description,recurrence_id=r_booking.id)
        for date in dates:
            self.create(room_id=room_id,date=date,start_time=start,end_time=end,contact=contact,description=description,recurrence_id=r_booking.id)
        return booking

    def isRecurring(self,id):
        return self.get_queryset().isRecurring(id)

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
        return self.get_queryset().formatDate(id)

class RoomsQueryset(models.query.QuerySet):
    def get_name(self,id):
        query = self.get(room_id=id)
        return query.room_name

class RoomsManager(models.Manager):
    def get_queryset(self):
        return RoomsQueryset(self.model, using=self._db)

    def get_name(self,id):
        return self.get_queryset().get_name(id)
