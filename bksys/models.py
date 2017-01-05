from django.db import models
from datetime import datetime

class rooms(models.Model):
	room_id         = models.AutoField(primary_key=True)
	room_name       = models.CharField(max_length=60, null = False)
	room_size       = models.IntegerField(null = False)
	room_location   = models.TextField(null = False)
	room_features   = models.TextField(null = False)
	in_use 			= models.BooleanField(default=True)

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
	room       	    = models.ForeignKey(rooms,  on_delete=models.CASCADE, null = False)
	expiry 			= models.DateTimeField(auto_now_add=True)

class bookings(models.Model):
	booking_ref = models.AutoField(primary_key=True)
	room        = models.ForeignKey(rooms,  on_delete=models.CASCADE, null = False)
	date        = models.DateField(null=False)
	start_time  = models.TimeField(null = False)
	end_time    = models.TimeField(null = False)
	contact     = models.CharField(max_length=60, null = False)
	description = models.CharField(max_length=60, null = False)

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
