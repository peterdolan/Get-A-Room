from rest_framework import serializers
from booker.models import UserProfile, Group

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ('id','first_name', 'last_name', 'groups', 'organizations', 'groups', 'picture',)

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id','name', 'admins', 'nres', 'member_requests',)

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id','name', 'admins',)

class BuildingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id','name', 'admins', 'nres', 'member_requests',)