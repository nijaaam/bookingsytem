from django.db import models
from bksys.managers import *
from datetime import datetime, timedelta
from django.utils import timezone

class rooms(models.Model):
    room_id         = models.AutoField(primary_key=True)
    room_name       = models.CharField(max_length=60, null = False)
    room_size       = models.IntegerField(null = False)
    room_location   = models.CharField(max_length=240, null = False)
    room_features   = models.CharField(max_length=240, null = False)
    in_use          = models.BooleanField(default=True)
    objects = RoomsManager()
    
    class Meta:
        db_table = "rooms"

class reservations(models.Model):
    room               = models.OneToOneField(rooms,  on_delete=models.CASCADE, null = False)
    start_time         = models.DateTimeField(auto_now_add=True)
    session_id         = models.CharField(max_length=240,null=False)
    
    class Meta:
        db_table = "reservations"

class recurringEvents(models.Model):
    start_date = models.DateField(null = False)
    end_date = models.DateField(null = False)
    recurrence_options = (
        ('1','Daily'),
        ('2','Weekly'),
        ('3',"Biweekly"),
    )
    recurrence = models.CharField(max_length=10,choices=recurrence_options)
    objects = recurringEventsManager()
    class Meta:
        db_table = "recurringEvents"

class users(models.Model):
    name = models.CharField(max_length=254, null=False)
    email = models.EmailField(max_length=70,null=False,unique=True)
    passcode = models.CharField(max_length=254,unique=True)
    objects = UserManager()
    
    class Meta:
        db_table = "user"

class bookings(models.Model):
    booking_ref = models.AutoField(primary_key=True)
    user        = models.OneToOneField(users,  on_delete=models.CASCADE, null = False)
    room        = models.OneToOneField(rooms,  on_delete=models.CASCADE, null = False)
    recurrence  = models.OneToOneField(recurringEvents,  on_delete=models.CASCADE, null = True)
    date        = models.DateField(null = False)
    start_time  = models.TimeField(null = False)
    end_time    = models.TimeField(null = False)
    contact     = models.CharField(max_length=60, null = False)
    description = models.CharField(max_length=60, null = False)
    objects = BookingsManager()

    class Meta:
        db_table = "bookings"
    
