from django.views.generic import TemplateView
from django.shortcuts import render, redirect


# Create your views here.
class port_view(TemplateView):
	template_name = 'portfolio/home.html'

