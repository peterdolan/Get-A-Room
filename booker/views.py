from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import *

def index(request):
    reservation_list = Reservation.objects.all()
    context = {'reservation_list': reservation_list}
    return render(request, 'booker/index.html', context)
