from django.contrib import admin

from .models import *

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Group)
