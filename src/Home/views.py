# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from .forms import SignUpForm
from .models import SignUp

# Create your views here.

def home(request):
	queryset = SignUp.objects.all()
	context = {
		"object_lists": queryset,
		"title": "Seer Home",
	}
	return render(request, 'home/home.html', context)

def team(request):
	return render(request, 'home/team.html')

def register(request):
	form = SignUpForm(request.POST or None)

	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()

	return render(request, 'home/register.html', {'form': form})

def login(request, id):
	instance = get_object_or_404(Post, id=id)
	
	return render(request, 'home/login.html')

def logout(request):
	return redirect('/login/')
