from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import SignUpForm, EditProfileForm, DeleteProfileForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse

# Create your views here.
def home(request):
	return render(request, 'home/home.html')

def team(request):
	return render(request, 'home/team.html')

def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		
		if form.is_valid():
			form.save()
			return redirect('/home')

	else:
		form = SignUpForm()
		return render(request, 'home/register.html', {'form': form})

def view_profile(request):
	context = {'user': request.user}
	return render(request, 'home/profile.html', context)

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect('/profile')

	else:
		form = EditProfileForm(instance=request.user)
		return render(request, 'home/edit.html', {'form': form, 'user': request.user})

def delete_person(request, person_pk):
    query = User.objects.get(pk=person_pk)
    query.delete()
    return HttpResponse("Deleted!")
