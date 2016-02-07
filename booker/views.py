from datetime import datetime, date, time, timedelta
from sets import Set

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
			return render(request, 'booker/result.html', {'rooms':rooms, 'form':form})
	else:
		form = RoomForm()
	return render(request, 'booker/index.html', {'form':form})


def getValidRooms(request, form):
	# date = datetime.datetime(form.cleaned_data['date'])
	date = form.cleaned_data['date']
	start_time = form.cleaned_data['time']
	duration = form.cleaned_data['duration']
	capacity = int(form.cleaned_data['capacity'])
	projector_bool = bool(form.cleaned_data['projector'])
	whiteboard_bool = bool(form.cleaned_data['whiteboard'])
	windows_bool = bool(form.cleaned_data['windows'])

	kwargs = {
		'capacity__gte':capacity,
	}
	if projector_bool:
		kwargs['has_projector'] = True
	if windows_bool:
		kwargs['has_windows'] = True
	if whiteboard_bool:
		kwargs['has_whiteboard'] = True
	room_objects_filtered = Room.objects.all().filter(**kwargs)

	# res = Reservation.objects.all()
	# bldgs = Building.objects.all()
	start_time = getActualDate(date,start_time)
	# dur_dt = timedelta(0)
	if duration == "thirty":
		dur_dt = timedelta(minutes=30)
	elif duration == "one":
		dur_dt = timedelta(hours=1)
	elif duration == "two":
		dur_dt = timedelta(hours=2)
	else: #as long as u want??
		dur_dt = timedelta(hours=3)
	end_time = start_time + dur_dt
	time_tuple = (start_time, end_time)
	return checkReservations(room_objects_filtered, time_tuple)


def checkReservations(room_objects_list, time_tuple):
	#look for overlap by comparing reservation times to times desired
	#any rooms taken for time slice x are taken off the available rooms list
	
	reservations_case1 = Reservation.objects.all().filter(start_time__lte=time_tuple[0],end_time__gte=time_tuple[1])
	reservations_case2 = Reservation.objects.all().filter(start_time__lte=time_tuple[0],end_time__gte=time_tuple[0],end_time__lte=time_tuple[1])
	reservations_case3 = Reservation.objects.all().filter(start_time__gte=time_tuple[0],start_time__lte=time_tuple[1],end_time__gte=time_tuple[1])
	reservations_case4 = Reservation.objects.all().filter(start_time__gte=time_tuple[0],end_time__lte=time_tuple[1])

	overlapped_room_names = Set()
	for res in reservations_case1:
		overlapped_room_names.add(res.room)
	for res in reservations_case2:
		overlapped_room_names.add(res.room)
	for res in reservations_case3:
		overlapped_room_names.add(res.room)
	for res in reservations_case4:
		overlapped_room_names.add(res.room)

	#HOW TO CHECK WHATS IN HERE?
	#NEED TO DEBUG
	available_rooms_list = []
	for room_obj in room_objects_list:
		if room_obj.name not in overlapped_room_names:
			available_rooms_list.append(room_obj)
	return available_rooms_list

def getActualDate(date_str, time_str):
	#first date
	timestamp = date.today()
	if date_str == "tomorrow":
		timestamp = datetime.timedelta(days=1)
	elif date_str == "two": #two
		timestamp += datetime.timedelta(days=2)
	#now times
	if time_str == "thirty":
		timestamp += datetime.timedelta(minutes=30)
	elif time_str == "one":
		timestamp += datetime.timedelta(hours=1)
	elif time_str == "two": #two hrs
		timestamp += datetime.timedelta(hours=2)
	return timestamp

def confirm(request, name):
	#do work to get all info about the room so we can display on html page
	room_obj = Room.objects.all().filter(name=name)[0]
	user_obj = []

	# NEED to get real start/end times!!
	fake_start_time = datetime.today()
	fake_end_time = fake_start_time + timedelta(hours=1)
	#insert into database
	res = Reservation.objects.get_or_create(room=room_obj, user_name='Alec Powell', user_email='atpowell@stanford.edu', description='!!', start_time=fake_start_time, end_time=fake_end_time)[0]
	return render(request, 'booker/confirm.html', {'name':name, 'res_object':res})
