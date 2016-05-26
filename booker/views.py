from datetime import datetime, date, time, timedelta
from itertools import chain
from sets import Set
import pytz
import json

from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from booker.forms import UserForm, UserProfileForm, ChangePasswordForm, ChangeProfilePictureForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *
from .forms import *

@login_required
def index(request):
	if request.method == 'POST':
		form = RoomForm(request.POST)
		if form.is_valid():
			nmeetings = form.cleaned_data['nmeetings']
			if nmeetings is None or not form.cleaned_data['weekly']:
				nmeetings = 1
			rooms = getValidRooms(form, nmeetings)
			suggested = False
			if not rooms:
				suggested = True
				rooms = getSuggestionRoomObjects(form, nmeetings, 0)
			return render(request, 'booker/result.html', {'rooms':rooms, 'form':form, 'nmeetings':nmeetings, 'suggested':suggested})

	else:
		form = RoomForm()
		if request.session.get('group_search', False):
			group = Group.objects.all().filter(name=request.session.get('group'))[0]
			if group.nres < 10:
				form.fields['nmeetings'].initial = group.nres

	return render(request, 'booker/index.html', {'form':form, 'group_search':request.session.get('group_search', False), 'group':request.session.get('group', '')})

def getValidRooms(form, nmeetings):
	date = form.cleaned_data['date']
	start_time = form.cleaned_data['time']
	duration = form.cleaned_data['duration']
	capacity = int(form.cleaned_data['capacity'])
	projector_bool = bool(form.cleaned_data['projector'])
	whiteboard_bool = bool(form.cleaned_data['whiteboard'])
	windows_bool = bool(form.cleaned_data['windows'])
	area = form.cleaned_data['area']

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
	return checkReservations(room_objects_ordered, time_tuple, nmeetings)

def getSuggestionRoomObjects(form, nmeetings, it):
	print 'Looking for rooms again. Iteration: ' + str(it)
	capacity = int(form.cleaned_data['capacity'])
	projector_bool = bool(form.cleaned_data['projector'])
	whiteboard_bool = bool(form.cleaned_data['whiteboard'])
	windows_bool = bool(form.cleaned_data['windows'])

	kwargs = {}
	if it == 0:
		kwargs['capacity__gte'] = 0
		if projector_bool:
			kwargs['has_projector'] = True
		if windows_bool:
			kwargs['has_windows'] = True
		if whiteboard_bool:
			kwargs['has_whiteboard'] = True
		it = 1
	elif it == 1:
		kwargs['capacity__gte'] = capacity
		if projector_bool:
			kwargs['has_projector'] = False
			if windows_bool:
				kwargs['has_windows'] = True
			if whiteboard_bool:
				kwargs['has_whiteboard'] = True
			it = 2
		else:
			if windows_bool:
				kwargs['has_windows'] = False
				if whiteboard_bool:
					kwargs['has_whiteboard'] = True
				it = 3
			else:
				if whiteboard_bool:
					kwargs['has_whiteboard'] = False
					it = -1
				else:
					rooms = []
					return rooms
	elif it == 2:
		kwargs['capacity__gte'] = capacity
		if projector_bool:
			kwargs['has_projector'] = True
		if windows_bool:
			kwargs['has_windows'] = False
			if whiteboard_bool:
				kwargs['has_whiteboard'] = True
			it = 3
		else:
			if whiteboard_bool:
				kwargs['has_whiteboard'] = False
				it = -1
			else:
				rooms = []
				return rooms
	elif it == 3:
		kwargs['capacity__gte'] = capacity
		if projector_bool:
			kwargs['has_projector'] = True
		if windows_bool:
			kwargs['has_windows'] = True
		if whiteboard_bool:
			kwargs['has_whiteboard'] = False
			it = -1
		else:
			rooms = []
			return rooms
	else: 
		rooms = []
		return rooms

	date = form.cleaned_data['date']
	start_time = form.cleaned_data['time']
	duration = form.cleaned_data['duration']
	area = form.cleaned_data['area']

	room_objects_filtered = Room.objects.all().filter(**kwargs)
	room_objects_ordered = room_objects_filtered.order_by('name')

	start_time = getActualDate(date,start_time)
	dur_dt = timedelta(minutes=int(duration))
	end_time = start_time + dur_dt
	time_tuple = (start_time, end_time)
	room_list = checkReservations(room_objects_ordered, time_tuple, nmeetings)
	if room_list:
		print 'Found something.'
		return room_list
	else:
		print  "Didn't find anything. Going to new iteration."
		return getSuggestionRoomObjects(form, nmeetings, it)
		

def checkReservations(room_objects_list, time_tuple, nmeetings):
	#look for overlap by comparing reservation times to times desired
	#any rooms taken for time slice x are taken off the available rooms list
	available_rooms_list = []

	for room_obj in room_objects_list:
		is_valid_flag = True
		room_reservation_list = Reservation.objects.all().filter(room=room_obj)
		for res_obj in room_reservation_list:
			if checkValidRes(res_obj, time_tuple, nmeetings) == False: #we have an overlapping reservation
				is_valid_flag = False
				break
		if is_valid_flag:
			available_rooms_list.append(room_obj)

	# reservations = Reservation.objects.all().filter(~(st_queryfilter1 | st_queryfilter2) & (et_queryfilter1 | et_queryfilter2))
	return available_rooms_list

def checkValidRes(res_obj, time_tuple, nmeetings):
	res_start = res_obj.start_time
	res_end = res_obj.end_time
	for x in range(0, nmeetings):
		offset = 7*x
		request_start = time_tuple[0] + timedelta(days=offset)
		request_end = time_tuple[1] + timedelta(days=offset)
		if not (((request_start < res_start) or (request_start > res_end)) and ((request_end < res_start) or (request_end > res_end))):
			return False
	return True

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

	print "In post_rez"
	form = ReservationForm(request.POST)
	if form.is_valid():
		print "form is valid"
		room_obj = Room.objects.all().filter(name=form.cleaned_data['room'])[0]
		res_start_time = getActualDate(form.cleaned_data['date'],form.cleaned_data['time'])
		duration = form.cleaned_data['duration']
		dur_dt = timedelta(minutes = int(duration))
		res_end_time = res_start_time + dur_dt
		res_ids = []
		print "about to build rezzies"
		description = form.cleaned_data['description']
		for x in range(0, int(form.cleaned_data['nmeetings'])):
			offset = 7*x
			group = None
			if request.session.get('group_search', False):
				print "Tis a group search"
				print request.session.get('group')
				group = Group.objects.all().filter(name=request.session.get('group', None))[0]
				print "Got the group"
			res = Reservation.objects.get_or_create(room=room_obj, user=request.user.userprofile, group=group, description=description, start_time=res_start_time+timedelta(days=offset), end_time=res_end_time+timedelta(days=offset))[0]
			res_ids.append(res.id)
		print "Built rezzies"
		request.session['res_ids'] = res_ids
		request.session['first_confirm'] = True
		if request.session.get('group_search', False):
			group = Group.objects.all().filter(name=request.session.get('group', None))[0]
			print "GOT GROUP " + group.name
			group.nres = group.nres - int(form.cleaned_data['nmeetings'])
			group.save()
		return HttpResponseRedirect('/booker/confirm/')
	else:
		return render(request, 'booker/uhmmm.html')

def confirm(request):
	if (request.session.get('first_confirm', False)):
		group_search = request.session.get('group_search')
		group = request.session.get('group')
		res_ids = request.session.get('res_ids', [])
		request.session['group_search'] = False
		request.session['group'] = ""
		request.session['res_ids'] = []
		request.session['first_confirm'] = False
		reservations = []
		for res_id in res_ids:
			res = Reservation.objects.all().get(pk=res_id)
			reservations.append(res)
		return render(request, 'booker/confirm.html', {'reservations': reservations, 'room':res.room.name, 'building':res.room.building.name, 'group_search':group_search, 'group':group})

	else:
		return HttpResponseRedirect('/booker/profile/')

def calendar_view(request):
	context = RequestContext(request)
	# if request.method == 'POST':
		# form = CalendarViewForm(data=request.POST)
		# if form.is_valid():
	profile = request.user.userprofile
	organizations = profile.organizations.all()
	buildings = Building.objects.all().filter(organization__in=organizations)
	rooms_list = Room.objects.all().filter(building__in=buildings)
	res_array = Reservation.objects.all().filter(room__in=rooms_list, start_time__gte=timezone.now())

	return render(request, 'booker/calendar.html', {'buildings':buildings, 'res_array':res_array})

def buildings(request):
	profile = request.user.userprofile
	organizations = profile.organizations.all()
	buildings = Building.objects.all().filter(organization__in=organizations)
	building_map = {}
	for building in buildings:
		rooms_list = [str(x) for x in Room.objects.all().filter(building=building).values_list('name',flat=True)]
		building_map[building.name] = rooms_list
	return HttpResponse(json.dumps(building_map))

def get_closest_reservation(request):
	date = request.POST.get('date', False)
	room = request.POST.get('room', False)
	date = date.split(" GMT")[0]
	new_date = datetime.strptime(date, "%a %b %d %Y %H:%M:%S")
	room_obj = Room.objects.all().filter(name=room)[0]
	reservations = Reservation.objects.all().filter(room=room_obj, start_time__gt=new_date).order_by('start_time')
	if not reservations:
		return HttpResponse(-1)
	else: 
		reservation = reservations[0]
		time = str(reservation.start_time)
		time = time[:-6]
		time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
		json_data = {}
		json_data['year'] = time.year
		json_data['month'] = time.month
		json_data['day'] = time.day
		json_data['hour'] = time.hour
		json_data['minute'] = time.minute
		json_data['second'] = time.second
		json_encoded = json.dumps(json_data)
		return HttpResponse(json_encoded)

# def get_room_info(request):
# 	room_name = request.GET.get('room', False)
# 	building_name = request.GET.get('building', False)

def eventsFeed(request, room_name):
	from django.utils.timezone import utc

	try:
		start = datetime.fromtimestamp(int(request.GET.get('start', False))).replace(tzinfo=utc)
		end = datetime.fromtimestamp(int(request.GET.get('end',False)))
	except ValueError:
		start = datetime.now.replace(tzinfo=utc)
		end = start + timedelta(days=7)

	room_obj = Room.objects.all().filter(name=room_name)
	entries = Reservation.objects.all().filter(room=room_obj, start_time__gte=start).filter(end_time__lte=end)
	json_list = []
	for entry in entries:
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

def getOnOrganizations(orgs):
	o = []
	for org in orgs:
		if org.on:
			o.append(org)
	return o

@login_required
def user_profile(request):
	# Handles reloading and automatically navigating to a given tab
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
	# Profile of the current user
	profile = request.user.userprofile
	# User's profile picture
	profile_pic = profile.get_profile_pic_url()
	# Reservations under this user's name
	personal_reservations = Reservation.objects.filter(user=profile,group__isnull=True,end_time__gte=datetime.today()- timedelta(hours=8))
	# Reservations for groups this user is a member of
	group_reservations = Reservation.objects.filter(group__in=profile.groups.all(),end_time__gte=datetime.today()- timedelta(hours=8))
	# Sorts group reservations by group name, breaks ties with start time
	group_reservations = sorted(group_reservations, key=lambda x: (x.group.name, x.start_time))
	# Final reservation list (personal+group)
	reservations = list(chain(personal_reservations,group_reservations))
	print reservations
	# Groups this user is an admin of
	admin_groups = profile.admin_of.all()
	# Groups this user is a member of
	groups = profile.groups.all()

	# Organizations this user is an admin of and that are "on"
	admin_organizations = profile.get_admin_organizations()
	admin_organizations = getOnOrganizations(admin_organizations)

	# Organizations this user is a member of and that are "on"
	organizations = profile.organizations.all()
	organizations = getOnOrganizations(organizations)

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


def groupres(request):
	if request.method == 'POST':
		form = GroupReservationForm(request.POST)
		if form.is_valid():
			request.session['group'] = form.cleaned_data['group']
			request.session['group_search'] = True
			return HttpResponseRedirect('/booker/')

	return HttpResponseRedirect('/ummmm/')

def singleres(request):
	request.session['group'] = ""
	request.session['group_search'] = False
	return HttpResponseRedirect('/booker/')

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

		# is this necessary anymore?
		admin.is_group_admin = True

		admin.groups.add(group)
		group.save()
		admin.save()

	return HttpResponse(0)

@login_required
@ensure_csrf_cookie
def create_organization(request):
	if request.method == 'POST':
		print request.POST.get('org_name')
		org_name = request.POST.get('org_name')
		org = Organization(name=org_name)
		org.save()
		admin = request.user.userprofile
		org.admins.add(admin)
		admin.organizations.add(org)
		org.save()
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
		reservations = Reservation.objects.all().filter(pk__in=reservation_ids)
		for res in reservations:
			if res.group:
				print "GROUP NAME: " + res.group.name
				group = res.group
				group.nres = group.nres + 1
				group.save()
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
def groups(request):
	if request.method == "GET":
		return HttpResponse(serializers.serialize('json',Group.objects.all()))

@ensure_csrf_cookie
def organizations(request):
	if request.method == "GET":
		return HttpResponse(serializers.serialize('json',Organization.objects.all()))

@ensure_csrf_cookie
def user_profiles(request):
	if request.method == "GET":
		return HttpResponse(serializers.serialize('json',UserProfile.objects.all()))

@ensure_csrf_cookie
def join_group_request(request):
	if request.method == 'POST':
		group_name = request.POST.get('group_name')
		group = Group.objects.get(name=group_name)
		group.member_requests.add(request.user.userprofile)
		group.save()
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

@ensure_csrf_cookie
def add_user_to_group(request):
	if request.method == 'POST':
		group_name = request.POST.get('group_name')
		group = Group.objects.get(name=group_name)
		user_profile_pk = int(request.POST.get('user_profile_pk'))
		user_profile = UserProfile.objects.get(pk=user_profile_pk)
		user_profile.groups.add(group)
		user_profile.save()

	return HttpResponse(0)

@ensure_csrf_cookie
def add_group_admin(request):
	if request.method == 'POST':
		group_name = request.POST.get('group_name')
		group = Group.objects.get(name=group_name)
		user_profile_pk = int(request.POST.get('user_profile_pk'))
		user_profile = UserProfile.objects.get(pk=user_profile_pk)
		group.admins.add(user_profile)
		group.save()

	return HttpResponse(0)

@ensure_csrf_cookie
def user(request):
	if request.method == 'GET':
		user_serializable = {}
		user_profile = UserProfile.objects.all().filter(user=request.user)[0]
		profile_picture_url = str(user_profile.get_profile_pic_url())

	return HttpResponse(profile_picture_url)

def settings(request):
	active_tab_array = ['','','','']
	active_tab = request.GET.get('tab')
	if active_tab is None:
		active_tab = 'password'
	if active_tab == 'password':
		active_tab_array[0] = ' active'
	elif active_tab == 'picture':
		active_tab_array[1] = ' active'
	elif active_tab == 'create':
		active_tab_array[2] = ' active'
	elif active_tab == 'contact':
		active_tab_array[3] = ' active'
	password_form = ChangePasswordForm()
	profile_form = ChangeProfilePictureForm()
	pic_url = request.user.userprofile.get_profile_pic_url()
	return render(request, 'booker/settings.html', {'pform':password_form, 'uform':profile_form, 'pic_url':pic_url, 'active_tab':active_tab_array})

def change_password(request):
	if request.method == 'POST':
		oldp = request.POST.get('oldp')
		newp = request.POST.get('newp')
		user = authenticate(username=request.user.username, password=oldp)
		if user:
			if user.is_active:
				user.set_password(newp)
				user.save()
				login(request, user)
				return HttpResponse(200)

	return HttpResponseBadRequest(401)

def change_profile_picture(request):
	if request.method == 'POST':
		form = ChangeProfilePictureForm(request.POST, request.FILES)
		if form.is_valid():
			profile = request.user.userprofile
			profile.picture = request.FILES['picture']
			profile.save()
			return HttpResponseRedirect('/booker/settings/?tab=picture')
	return HttpResponseBadRequest(401)






	

