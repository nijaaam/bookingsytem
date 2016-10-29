from django.db import models

# Create your models here.
class bookings(mode.Model):
	booking_ref = models.CharField()
	room_id     = models.IntegerField()
	date        = models.DateField()
	start_time  = models.TimeField()
	end_time    = models.TimeField()
	duration    = models.DurationField()
