from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import *
from .forms import TimeForm


def index(request):

	if request.method == 'POST':
		form = TimeForm(request.POST)
		if form.is_valid():
			return render(request, 'booker/result.html', {'date':form.cleaned_data['date'],
														  'time':form.cleaned_data['time'],
														  'duration':form.cleaned_data['duration'],
														  'projector':form.cleaned_data['projector'],
														  'whiteboard':form.cleaned_data['whiteboard'],
														  'windows':form.cleaned_data['windows']})
	else:
		time_form = TimeForm()
	return render(request, 'booker/index.html', {'time_form':time_form})


	
