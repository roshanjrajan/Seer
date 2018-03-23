from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# custom forms
class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
		)

	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

class EditProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'email',
			'password',
			# 'timestamp'
		)

class DeleteProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields = '__all__'
