# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse, render, redirect
from .forms import SignUpForm

# Create your views here.

def home(request):
	return render(request, 'home/default.html')

def team(request):
	return render(request, 'home/team.html')

def register(request):
	form = SignUpForm(request.POST or None)

	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()

	return render(request, 'home/register.html', {'form': form})

def login(request):
	return render(request, 'home/login.html')

def logout(request):
	return redirect('/login/')
