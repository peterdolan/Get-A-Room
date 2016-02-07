from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import *
from .forms import TimeForm


def index(request):

	if request.method == 'POST':
		form = TimeForm(request.POST)
		if form.is_valid():
			rooms = Room.objects.all()
			return render(request, 'booker/result.html', {'rooms': rooms})
	else:
		time_form = TimeForm()
	return render(request, 'booker/index.html', {'time_form':time_form})


	
