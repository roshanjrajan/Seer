from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .tokens import account_activation_token
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
			user = form.save(commit=False)
			user.is_active = False
			user.save()

			current_site = get_current_site(request)
			subject = 'Activate Your MySite Account'
			message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
			from_email = settings.EMAIL_HOST_USER
			to_list = [user.email, settings.EMAIL_HOST_USER]
			# user.email_user(subject, message)
			send_mail(subject, message, from_email, to_list, fail_silently=True)

			messages.success(request, 'Thank you for joining Seer. Please check you email to activate your account.')
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


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.userprofile.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('/portfolio/')
	else:
		return render(request, 'account/login.html')

def account_activation_sent(request):
	return render(request, 'account/account_activation_sent.html')
