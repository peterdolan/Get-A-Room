from django import forms
from django.db import models
from functools import partial
from datetime import datetime
import time
from booker.models import UserProfile, Group
from django.contrib.auth.models import User


def getStarterNum():
	# This function returns the time that should b shown initially
	t = time.localtime()
	h = t.tm_hour
	toReturn = (h - 7) # Accounts for tz
	toReturn = 2 * toReturn
	if(toReturn > 4 and toReturn < 16): # Times we don't have numbers
		toReturn = 16
	if(toReturn > 47):
		toReturn = 0
	return toReturn

class RoomForm(forms.Form):
	date = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'datepicker'})
	)
	
	time_choices = (
		(0, '12:00 AM'),
		(1, '12:30 AM'),
		(2, '1:00 AM'),
		(3, '1:30 AM'),
		(4, '2:00 AM'),
		(16, '8:00 AM'),
		(17, '8:30 AM'),
		(18, '9:00 AM'),
		(19, '9:30 AM'),
		(20, '10:00 AM'),
		(21, '10:30 AM'),
		(22, '11:00 AM'),
		(23, '11:30 AM'),
		(24, '12:00 PM'),
		(25, '12:30 PM'),
		(26, '1:00 PM'),
		(27, '1:30 PM'),
		(28, '2:00 PM'),
		(29, '2:30 PM'),
		(30, '3:00 PM'),
		(31, '3:30 PM'),
		(32, '4:00 PM'),
		(33, '4:30 PM'),
		(34, '5:00 PM'),
		(35, '5:30 PM'),
		(36, '6:00 PM'),
		(37, '6:30 PM'),
		(38, '7:00 PM'),
		(39, '7:30 PM'),
		(40, '8:00 PM'),
		(41, '8:30 PM'),
		(42, '9:00 PM'),
		(43, '9:30 PM'),
		(44, '10:00 PM'),
		(45, '10:30 PM'),
		(46, '11:00 PM'),
		(47, '11:30 PM'),
	)

	time = forms.ChoiceField(
		label = "What Time?",
		required = False,
		choices = time_choices,
		initial = 26
	)

	duration_choices = (
		(30, '30 Minutes'),
		(60, '1 Hour'),
		(90, '90 Minutes'),
		(120, '2 Hours'),
		(150, '2.5 Hours'),
		(180, '3 Hours')
		# ('max', 'As long as possible')
	)
	duration = forms.ChoiceField(
		label = "Duration",
		required = False,
		choices = duration_choices,
		initial = 60
	)

	capacity = forms.IntegerField(
		label = "Group Size",
		min_value = 1,
		max_value = 20,
		initial = 3
	)

	weekly = forms.BooleanField(
		label = "Make Weekly",
		required = False,
		initial = False
	)

	nmeetings = forms.IntegerField(
		label = "Number of Weeks",
		min_value = 2,
		max_value = 10,
		initial = 10,
		required = False
	)

	# description = forms.CharField(
	# 	widget=forms.TextInput	
	# )

	projector = forms.BooleanField(
		required = False,
		initial = False,
		label = "Projector"
	)
	whiteboard = forms.BooleanField(
		required = False,
		initial = False,
		label = "Whiteboard"
	)
	windows = forms.BooleanField(
		required = False,
		initial = False,
		label = "Windows"
	)

	area_choices = (
		('empty', ''),
		('huang', 'Huang'),
		('quad', 'Main Quad'),
		('union', 'Old Union'),
		('any', 'Anywhere'),
		('other', 'Other')
	)
	area = forms.ChoiceField(
		label = "Where?",
		required = False,
		choices = area_choices
	)

	flexible = forms.BooleanField(
		required = False,
		initial = False,
		label = "Accept other locations?"
	)

class ReservationForm(forms.Form):
	room = forms.CharField(max_length=200)
	date = forms.CharField(max_length=200)
	time = forms.CharField(max_length=200)
	duration = forms.CharField(max_length=200)
	nmeetings = forms.CharField(max_length=200)
	# description = forms.CharField(max_length=200)

class GroupReservationForm(forms.Form):
	group = forms.CharField(max_length=200)

class CalendarViewForm(forms.Form):
	building_choices = (
		('Old Union', 'Old Union'),
		('Huang', 'Huang'),
		('Main Quad', 'Main Quad')
	)

	building = forms.ChoiceField(
		label = "Choose building",
		required = True,
		choices = building_choices
	)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','picture')

class ChangePasswordForm(forms.Form):
	password = forms.CharField(
		widget=forms.PasswordInput,
		label="Old password",
		required=True
	)

	new1 = forms.CharField(
		widget=forms.PasswordInput,
		label="New password",
		required=True
	)
	
	new2 = forms.CharField(
		widget=forms.PasswordInput,
		label="Confirm new password",
		required=True
	)

class ChangeProfilePictureForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture')
