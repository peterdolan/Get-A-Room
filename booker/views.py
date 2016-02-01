from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import *
from .forms import TimeForm

def index(request):

	if request.method == 'POST':
		form = TimeForm(request.POST)
		if form.is_valid():
			return render(request, 'booker/result.html', {'name':form.cleaned_data['date']})
   
	else:
		form = TimeForm()

	return render(request, 'booker/index.html', {'form':form})


	
