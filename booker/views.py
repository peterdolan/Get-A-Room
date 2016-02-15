from datetime import datetime, date, time, timedelta
from sets import Set

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from booker.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout

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
	room_objects_ordered = room_objects_filtered.order_by('name')

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
		res_start_time -= timedelta(hours=8)
		res_end_time = res_start_time + dur_dt
		#insert into database
		username = 'guest'
		useremail = 'atpowell@stanford.edu'
		if request.user.is_authenticated():
			username = request.user.username
			useremail = request.user.email
		res = Reservation.objects.get_or_create(room=room_obj, user_name=username, user_email=useremail, description='!!', start_time=res_start_time, end_time=res_end_time)[0]
		return render(request, 'booker/confirm.html', {'res':res})
	else:
		return render(request, 'booker/uhmmm.html')

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
            # username is just the email for that user
            username = email
            password = user_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
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
                return HttpResponse("Your Rango account is disabled.")
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
	profile = request.user.userprofile
	return render(request, 'booker/profile.html', {'profile':profile})

