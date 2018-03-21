# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse, render, redirect

# Create your views here.

def home(request):
	return HttpResponse("<h1>Welcome</h1>")

def team(request):
	return render(request, 'team.html')

def login(request):
	return render(request, 'login.html')
