from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from .models import rooms,bookings

def index(request):
	res = rooms.objects.all()
	return render_to_response('home.html', {'query_results': res})