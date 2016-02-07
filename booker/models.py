from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Building(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name


class Room(models.Model):
	name = models.CharField(max_length=200)
	building = models.ForeignKey(Building, on_delete=models.CASCADE)
	capacity = models.IntegerField(default=0)
	has_projector = models.BooleanField(default=False)
	has_windows = models.BooleanField(default=False)
	has_whiteboard = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Reservation(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	user_name = models.CharField(max_length=200)
	user_email = models.EmailField()
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

class AdminUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    organization = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username



