from datetime import datetime, date, time, timedelta
from sets import Set

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from .models import *
from .forms import RoomForm
from .forms import ReservationForm

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
	available_rooms_list = []

	for room_obj in room_objects_list:
		is_valid_flag = True
		room_reservation_list = Reservation.objects.all().filter(room=room_obj)
		for res_obj in room_reservation_list:
			if checkValidRes(res_obj, time_tuple) == False: #we have an overlapping reservation
				is_valid_flag = False
				break
		if is_valid_flag:
			available_rooms_list.append(room_obj)

	# reservations = Reservation.objects.all().filter(~(st_queryfilter1 | st_queryfilter2) & (et_queryfilter1 | et_queryfilter2))
	return available_rooms_list

def checkValidRes(res_obj, time_tuple):
	request_start = time_tuple[0]
	request_end = time_tuple[1]
	res_start = res_obj.start_time
	res_end = res_obj.end_time
	return ((request_start < res_start) or (request_start > res_end)) and ((request_end < res_start) or (request_end > res_end))

def getActualDate(date_str, time_str):
	#first date
	timestamp = timezone.now()
	if date_str == "tomorrow":
		timestamp += timedelta(days=1)
	elif date_str == "two": #two
		timestamp += timedelta(days=2)
	#now times
	if time_str == "thirty":
		timestamp += timedelta(minutes=30)
	elif time_str == "one":
		timestamp += timedelta(hours=1)
	elif time_str == "two": #two hrs
		timestamp += timedelta(hours=2)
	return timestamp

def confirm(request):
	form = ReservationForm(request.POST)
	if form.is_valid():
		room_obj = Room.objects.all().filter(name=form.cleaned_data['room'])[0]
		user_obj = []
		res_start_time = getActualDate(form.cleaned_data['date'],form.cleaned_data['time'])
		duration = form.cleaned_data['duration']
		if duration == "thirty":
			dur_dt = timedelta(minutes=30)
		elif duration == "one":
			dur_dt = timedelta(hours=1)
		elif duration == "two":
			dur_dt = timedelta(hours=2)
		else: #as long as u want??
			dur_dt = timedelta(hours=3)
		res_end_time = res_start_time + dur_dt
		#insert into database
		res = Reservation.objects.get_or_create(room=room_obj, user_name='Alec Powell', user_email='atpowell@stanford.edu', description='!!', start_time=res_start_time, end_time=res_end_time)[0]
		return render(request, 'booker/confirm.html', {'res':res})
	else:
		return render(request, 'booker/uhmmm.html')
