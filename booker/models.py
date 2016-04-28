from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def getCurDate():
	return (datetime.datetime.now(), "Today")

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The user's first name
    first_name = models.CharField(max_length=30)
    # The user's last name
    last_name = models.CharField(max_length=30)
    # Organizations the user is a member of
    organizations = models.ManyToManyField('Organization',null=True,blank=True)
    # Groups the user is a member of
    groups = models.ManyToManyField('Group',null=True,blank=True)
    # Profile picture
    picture = models.ImageField(upload_to='booker/static/images/profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

    def get_profile_pic_url(self):
    	if self.picture:
    		return self.picture.url[len('booker/static/'):]
    	else:
    		return None

    def get_admin_organizations(self):
    	return self.organization_set.all()

class Organization(models.Model):
	name = models.CharField(max_length=200)
	admins = models.ManyToManyField(UserProfile,null=True)

	def __str__(self):
		return self.name

class Building(models.Model):
	name = models.CharField(max_length=200)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.name

class Room(models.Model):
	name = models.CharField(max_length=200)
	# nice_name = models.CharField(max_length=200)
	building = models.ForeignKey(Building, on_delete=models.CASCADE)
	capacity = models.IntegerField(default=0)
	has_projector = models.BooleanField(default=False)
	has_windows = models.BooleanField(default=False)
	has_whiteboard = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def get_name(self):
		return str(self.name)

class Group(models.Model):
	name = models.CharField(max_length=200)
	# admins of this group
	# an admin user_profile can select the groups
	# they are an admin of via .admin_of.all()
	admins = models.ManyToManyField(UserProfile, related_name="admin_of")
	nres = models.PositiveSmallIntegerField(default=20)
	# Users requesting to join this group
	# a user_profile can select the groups
	# they are requesting to join via .group_requests.all()
	member_requests = models.ManyToManyField(UserProfile, related_name="group_requests",null=True)
	# vso = models.IntegerField()

	def get_member_count(self):
		return len(self.userprofile_set.all())

	def __str__(self):
		return self.name

class Reservation(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
	description = models.TextField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	def get_string(self):
		return self.user_name + ' has booked ' + self.room.name + ' for ' + self.description
	#+ ' from ' + str(start_time) + ' to ' + str(end_time)

	# def __str__(self):
	# 	return ' '.join([
	# 		self.room.name,
	# 		self.user_name,
	# 	])





