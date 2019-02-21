# Django imports
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Inner app imports
from .models import (SiteCarousel, DynamicData,)

# Constants
USER_ROLES = {
  ('Blog Creator', 'Blog Creator'),
  ('Event Creator', 'Event Creator'),}


class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SubscriberForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True}))
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError("A subscriber with that email already exists")
		return email


class UserAccountForm(UserCreationForm):
	role = forms.ChoiceField(choices=USER_ROLES, initial='Blog Creator',
		widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'User Role'}))

	class Meta:
		model = User
		fields = ('username', 'role',)


class SiteCarouselForm(forms.ModelForm):
	class Meta:
		model = SiteCarousel
		fields = ('image',)


class DynamicDataForm(forms.ModelForm):
	class Meta:
		model = DynamicData
		fields = (
			'become_a_sponsor_url', 'become_a_volunteer_url', 'speaker_request_url', 'media_kit_url', 'photo_gallery_url',
			'about_us', 'google_plus_link', 'facebook_link', 'twitter_link', 'youtube_link', 'instagram_link', 'meetup_link',)