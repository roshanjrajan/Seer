from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, EditProfileForm


# Create your views here.
def home(request):
	return render(request, 'account/home.html')

def team(request):
	return render(request, 'account/team.html')

def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		
		if form.is_valid():
			form.save()
			return redirect('/account/login/')
		else:
			form = SignUpForm()
			return render(request, 'account/register.html', {'form': form})
	
	else:
		form = SignUpForm()
		return render(request, 'account/register.html', {'form': form})

@login_required
def view_profile(request):
	context = {'user': request.user}
	return render(request, 'account/profile.html', context)

@login_required
def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect('/account/profile')

	else:
		form = EditProfileForm(instance=request.user)
		return render(request, 'account/edit.html', {'form': form })

@login_required
def delete_profile(request, person_pk):
    query = User.objects.get(pk=person_pk)
    query.delete()
    return redirect('/account/register/')
