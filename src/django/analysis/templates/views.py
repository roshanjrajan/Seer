from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

def analysis(request):
	return render(request, 'analysis/analysis.html')

def analysisCurrency(request):
	return render(request, 'analysis/analysis/currency.html')
	# but there should be different pages for each currency?
