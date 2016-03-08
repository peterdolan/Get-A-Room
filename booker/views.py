from datetime import datetime, date, time, timedelta
from sets import Set
import pytz
import json

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from booker.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import ensure_csrf_cookie
import json

from .models import *
from .forms import *

# @login_required
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
	print date
	print start_time
	print duration
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
	room_objects_ordered = room_objects_filtered.order_by('name')

	start_time = getActualDate(date,start_time)
	dur_dt = timedelta(minutes=int(duration))
	end_time = start_time + dur_dt
	time_tuple = (start_time, end_time)
	return checkReservations(room_objects_ordered, time_tuple)

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

def zeroPad(toPad):
	if(len(toPad) == 1):
		return "0" + toPad
	return toPad

def getActualDate(date_str, time_str):
	utc = pytz.UTC
	hourString = zeroPad(str(int(time_str)/2))
	minuteString = zeroPad(str((int(time_str)%2) * 30))
	timeStamp = str(date_str) + " " + hourString + ":" + minuteString
	date = datetime.strptime(timeStamp, "%m/%d/%Y %H:%M")
	return utc.localize(date)

def post_reservation(request):
	form = ReservationForm(request.POST)
	if form.is_valid():
		room_obj = Room.objects.all().filter(name=form.cleaned_data['room'])[0]
		user_obj = []
		res_start_time = getActualDate(form.cleaned_data['date'],form.cleaned_data['time'])
		print "Start time: ", res_start_time
		duration = form.cleaned_data['duration']
		dur_dt = timedelta(minutes = int(duration))
		res_end_time = res_start_time + dur_dt
		# description = form.cleaned_data['description']
		res = Reservation.objects.get_or_create(room=room_obj, user=request.user.userprofile, description="!!", start_time=res_start_time, end_time=res_end_time)[0]
		request.session['res_id'] = res.id
		return HttpResponseRedirect('/booker/confirm/')
	else:
		return render(request, 'booker/uhmmm.html')

def confirm(request):
	res_id = request.session.get('res_id', None)
	res = Reservation.objects.all().get(pk=res_id)
	context = RequestContext(request)
	return render_to_response('booker/confirm.html', {'res':res},context)

def calendar_view(request):
	context = RequestContext(request)
	if request.method == 'POST':
		form = CalendarViewForm(data=request.POST)
		if form.is_valid():
			building_obj = Building.objects.all().filter(name__contains=form.cleaned_data['building'])[0]
			rooms_list = Room.objects.all().filter(building=building_obj)
			res_array = Reservation.objects.all().filter(room__in=rooms_list, start_time__gte=timezone.now())
			return render(request, 'booker/calendar.html', {'form':form, 'building':building_obj, 'res_array':res_array})
		else:
			return render(request, 'booker/uhmmm.html')
	else: #GET
		form = CalendarViewForm(data=request.POST)
		return render(request, 'booker/calendar.html', {'form':form, 'res_array':[]})
		# return render_to_response('booker/calendar.html', {}, context)

def eventsFeed(request, building_name):
	from django.utils.timezone import utc
	from django.core.serializers.json import DjangoJSONEncoder

	# print building_name

	if request.is_ajax():
		print 'Its ajax from fullCalendar()'

	try:
		start = datetime.fromtimestamp(int(request.GET.get('start', False))).replace(tzinfo=utc)
		end = datetime.fromtimestamp(int(request.GET.get('end',False)))
	except ValueError:
		start = datetime.now.replace(tzinfo=utc)
		end = start + timedelta(days=7)

	# entries = Reservation.objects.filter(start_time__gte=start).filter(end_time__lte=end)
	building_objs = Building.objects.all().filter(name__contains=building_name)
	rooms_list = Room.objects.all().filter(building__in=building_objs)
	entries = Reservation.objects.all().filter(room__in=rooms_list, start_time__gte=start).filter(end_time__lte=end)
	print entries
	json_list = []
	for entry in entries:
		# id = entry.id
		room = entry.room
		username = entry.user.first_name + " " + entry.user.last_name
		description = entry.description
		start = entry.start_time.strftime("%Y-%m-%dT%H:%M:%S")
		end = entry.end_time.strftime("%Y-%m-%dT%H:%M:%S")
		allDay = False
		json_entry = {'start':start, 'end':end, 'allDay':allDay, 'title': description}
		json_list.append(json_entry)
	return HttpResponse(json.dumps(json_list), content_type='application/json')

@login_required
def admin_dashboard(request):
	return HttpResponse("TODO: Build admin dashboard!")

# taken from:
# http://www.tangowithdjango.com/book/chapters/login.html
def register(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False

	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		user_profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid...
		if user_form.is_valid() and user_profile_form.is_valid():
			# Save the user's form data to the database.
			email = user_form.cleaned_data['email']

			user = None
			try:
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				user = None

			if user:
				return HttpResponse('User with that email already exists!!')
			# username is just the email for that user
			# username = email
			password = user_form.cleaned_data['password']
			# user = User.objects.create_user(username, email, password)
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			user = User.objects.get(pk=user.id)
			user.username = email
			user.save()

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = user_profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()

			# Update our variable to tell the template registration was successful.
			registered = True

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print user_form.errors, user_profile_form.errors

	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		user_profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render_to_response(
			'booker/register.html',
			{'user_form': user_form, 'user_profile_form': user_profile_form, 'registered': registered},
			context)


def user_login(request):
	# Like before, obtain the context for the user's request.
	context = RequestContext(request)

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/booker/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your Get-A-Room account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render_to_response('booker/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/booker/')

@login_required
def user_profile(request):
	active_tab_array = ['','','']
	active_tab = request.GET.get('tab')
	if active_tab is None:
		active_tab = 'reservation'

	if active_tab == 'reservation':
		active_tab_array[0] = ' active'
	elif active_tab == 'group':
		active_tab_array[1] = ' active'
	elif active_tab == 'organization':
		active_tab_array[2] = ' active'

	print active_tab_array

	profile = request.user.userprofile
	profile_pic = profile.get_profile_pic_url()
	reservations = Reservation.objects.all().filter(user=profile,end_time__gte=datetime.today()- timedelta(hours=8))
	admin_groups = []
	if profile.is_group_admin:
		admin_groups = profile.get_admin_groups()
	groups = profile.groups.all()
	print groups
	admin_organizations = []
	if profile.is_org_admin:
		admin_organizations = profile.get_admin_organizations()
	print "Admin Orgs", admin_organizations
	organizations = profile.organizations.all()
	# print organizations
	return render(request, 'booker/profile.html', {'profile':profile,
													'profile_pic':profile_pic,
													'reservations':reservations,
													'admin_groups':admin_groups,
													'groups':groups,
													'admin_organizations':admin_organizations,
													'organizations':organizations,
													'active_tab_array':active_tab_array
													})


@login_required
@ensure_csrf_cookie
def create_group(request):
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		print request.POST.get('group_name')
		group_name = request.POST.get('group_name')
		group = Group(name=group_name)
		group.save()
		admin = request.user.userprofile
		group.admins.add(admin)
		admin.is_group_admin = True
		admin.groups.add(group)
		admin.save()

	return HttpResponse(0)

@ensure_csrf_cookie
def delete_profile_info(request):
	if request.method == 'POST':
		# Get the current user's profile
		profile = request.user.userprofile

		# Delete reservation objects specified by reservation_ids
		reservation_ids_strs = json.loads(request.POST.get('reservation_ids'))
		reservation_ids = [int(x) for x in reservation_ids_strs]
		Reservation.objects.filter(pk__in=reservation_ids).delete()

		# Handle groups deleted from user's profile
		group_ids_strs = json.loads(request.POST.get('group_ids'))
		group_ids = [int(x) for x in group_ids_strs]
		for group_id in group_ids:
			group = Group.objects.get(pk=group_id)
			# Remove group from user's groupset
			profile.groups.remove(group)
			# If user is an admin for this group, remove user from group's admin set
			if profile in group.admins.all():
				group.admins.remove(profile)
				# If user is admin of no groups, turn off admin status
				if len(profile.group_set.all()) == 0:
					profile.is_group_admin = False
				# If group has no more admins, delete group
				if len(group.admins.all()) == 0:
					group.delete()

		# Handle orgs deleted from user's profile
		org_ids_strs = json.loads(request.POST.get('org_ids'))
		org_ids = [int(x) for x in org_ids_strs]
		for org_id in org_ids:
			org = Organization.objects.get(pk=org_id)
			# Remove group from user's groupset
			profile.organizations.remove(org)



	return HttpResponse(0)

@ensure_csrf_cookie
def get_group_list(request):
	all_group_names = []
	all_groups = Group.objects.all()
	for group in all_groups:
		all_group_names.append(group.name)
	print all_group_names
	print json.dumps(all_group_names)
	return HttpResponse(json.dumps(all_group_names))

@ensure_csrf_cookie
def get_org_list(request):
	all_org_names = []
	all_orgs = Organization.objects.all()
	for org in all_orgs:
		all_org_names.append(org.name)
	print all_org_names
	print json.dumps(all_org_names)
	return HttpResponse(json.dumps(all_org_names))

@ensure_csrf_cookie
def join_group(request):
	if request.method == 'POST':
		group_name = request.POST.get('group_name')
		group = Group.objects.get(name=group_name)
		request.user.userprofile.groups.add(group)
		# Reservation.objects.filter(pk__in=reservation_ids).delete()

	return HttpResponse(0)

@ensure_csrf_cookie
def join_org(request):
	if request.method == 'POST':
		org_name = request.POST.get('org_name')
		org = Organization.objects.get(name=org_name)
		request.user.userprofile.organizations.add(org)
		# Reservation.objects.filter(pk__in=reservation_ids).delete()

	return HttpResponse(0)




	

