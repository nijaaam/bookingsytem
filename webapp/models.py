from django.db import models

# Create your models here.
class bookings(models.Model):
	booking_ref = models.IntegerField()
	room_id     = models.IntegerField()
	date        = models.DateField()
	start_time  = models.TimeField()
	end_time    = models.TimeField()
	duration    = models.DurationField()

class rooms(models.Model):
	room_id         = models.IntegerField()
	room_name       = models.CharField(max_length=60)
	room_size       = models.IntegerField()
	room_location   = models.TextField()
	room_features   = models.TextField()

