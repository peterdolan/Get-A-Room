import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import models

from .models import *
from .forms import RoomForm


def index(request):

	if request.method == 'POST':
		form = RoomForm(request.POST)
		if form.is_valid():
			rooms = getValidRooms(request,form)
			print "!!"
			return render(request, 'booker/result.html', {'rooms':rooms, 'form':form})
	else:
		form = RoomForm()
	return render(request, 'booker/index.html', {'form':form})


def getValidRooms(request, form):
	# date = datetime.datetime(form.cleaned_data['date'])
	date = form.cleaned_data['date']
	start_time = form.cleaned_data['time']
	duration = form.cleaned_data['duration']
	capacity = 10 #CONSTANT FOR NOW
	projector_bool = bool(form.cleaned_data['projector'])
	whiteboard_bool = bool(form.cleaned_data['whiteboard'])
	windows_bool = bool(form.cleaned_data['windows'])

	# print Room.objects.all()
	room_objects = Room.objects.all()
	if projector_bool:
		if windows_bool:
			if whiteboard_bool:
				room_objects_filtered = Room.objects.all().filter(capacity__gte=capacity, has_projector=True, has_windows=True, has_whiteboard=True)
			else:
				room_objects_filtered = Room.objects.all().filter(capacity__gte=capacity, has_projector=True, has_windows=True)
		else:
			room_objects_filtered = Room.objects.all().filter(capacity__gte=capacity, has_projector=True)
	else:
		room_objects_filtered = Room.objects.all().filter(capacity__gte=capacity)



	# res = Reservation.objects.all()
	# bldgs = Building.objects.all()
	# fake_rooms = []
	# fake_rooms.append(getActualDate(date,start_time))
	# return fake_rooms
	return room_objects_filtered

def getActualDate(date_str, time_str):
	if date_str == "today":
		date = datetime.datetime.now()
	elif date_str == "tomorrow":
		date = datetime.datetime.now()
	else:
		date = datetime.datetime.now()
	return date

def confirm(request, name):
	return render(request, 'booker/confirm.html', {'name': name})
