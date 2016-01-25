from __future__ import unicode_literals

from django.db import models

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

	def __str__(self):
		return ' '.join([
			self.room.name,
			self.user_name,
			str(self.start_time),
			str(self.end_time)
		])


