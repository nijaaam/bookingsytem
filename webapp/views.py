from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import rooms,bookings

def index(request):
	res = rooms.objects.all()
	print (res[0].id)
	return render('home.html', {'query_results': res})