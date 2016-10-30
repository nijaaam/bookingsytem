from django.db import models

class rooms(models.Model):
	room_id         = models.IntegerField(primary_key =True, null = False)
	room_name       = models.CharField(max_length=60, null = False)
	room_size       = models.IntegerField(null = False)
	room_location   = models.TextField(null = False)
	room_avaliability   = models.TextField(null = False)
	room_features   = models.TextField(null = False)

class bookings(models.Model):
	booking_ref = models.IntegerField(primary_key =True, null = False)
	room_id     = models.ForeignKey(rooms,  on_delete=models.CASCADE, null = False)
	date        = models.DateField(null = False)
	start_time  = models.TimeField(null = False)
	end_time    = models.TimeField(null = False)
	duration    = models.DurationField(null = False)

