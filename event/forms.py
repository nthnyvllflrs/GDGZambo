import requests
# Django imports
from django import forms

# Inner App imports
from .models import (
	Sponsor, Speaker, Event, Feedback, EventStatistics, Info,
)


class SponsorForm(forms.ModelForm):
	class Meta:
		model = Sponsor
		fields = (
			'photo', 'name', 'email', 'description',
			'facebook', 'twitter', 'instagram', 'website', )
		widgets = {
			'name': forms.TextInput(attrs={'id': 'sponsor-name',}),
			'description': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'sponsor-description',}),
			'facebook': forms.TextInput(attrs={'id': 'sponsor-facebook',}),
			'twitter': forms.TextInput(attrs={'id': 'sponsor-twitter',}),
			'instagram': forms.TextInput(attrs={'id': 'sponsor-instagram',}),
			'website': forms.URLInput(attrs={'id': 'sponsor-website',}),}

	def clean_photo(self):
		return self.cleaned_data['photo'] or None

	def clean_facebook(self):
		facebook = self.cleaned_data['facebook']
		if facebook:
			request = requests.get('https://www.facebook.com/' + str(facebook))
			if request.status_code != 200:
				raise forms.ValidationError("Invalid Facebook Username")
		return facebook

	def clean_twitter(self):
		twitter = self.cleaned_data['twitter']
		if twitter:
			request = requests.get('https://www.twitter.com/' + str(twitter))
			if request.status_code != 200:
				raise forms.ValidationError("Invalid Twitter Username")
		return twitter

	def clean_instagram(self):
		instagram = self.cleaned_data['instagram']
		if instagram:
			request = requests.get('https://www.instagram.com/' + str(instagram))
			if request.status_code != 200:
				raise forms.ValidationError("Invalid Instagram Username")
		return instagram

class SpeakerForm(forms.ModelForm):
	class Meta:
		model = Speaker
		fields = (
			'photo', 'firstname', 'lastname', 'email', 'description', 
			'expertise', 'facebook', 'twitter', 'instagram', 'website',)

		widgets = {
			'firstname': forms.TextInput(attrs={'id': 'speaker-firstname'}),
			'lastname': forms.TextInput(attrs={'id': 'speaker-lastname'}),
			'email': forms.EmailInput(attrs={'id': 'speaker-email'}),
			'description': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'speaker-description',}),
			'expertise': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'speaker-expertise',}),
			'facebook': forms.TextInput(attrs={'id': 'speaker-facebook',}),
			'twitter': forms.TextInput(attrs={'id': 'speaker-twitter',}),
			'instagram': forms.TextInput(attrs={'id': 'speaker-instagram',}),
			'website': forms.URLInput(attrs={'id': 'speaker-website',}),
		}

	def clean_photo(self):
		return self.cleaned_data['photo'] or None

	def clean_facebook(self):
		facebook = self.cleaned_data['facebook']
		if facebook:
			request = requests.get('https://www.facebook.com/' + str(facebook))
			if request.status_code != 200:
				raise forms.ValidationError("Invalid Facebook Username")
		return facebook

	def clean_twitter(self):
		twitter = self.cleaned_data['twitter']
		if twitter:
			request = requests.get('https://www.twitter.com/' + str(twitter))
			if request.status_code != 200:
				raise forms.ValidationError("Invalid Twitter Username")
		return twitter

	def clean_instagram(self):
		instagram = self.cleaned_data['instagram']
		if instagram:
			request = requests.get('https://www.instagram.com/' + str(instagram))
			if request.status_code != 200:
				raise forms.ValidationError("Invalid Instagram Username")
		return instagram

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = (
			'title', 'description', 'meetup_ID',
			'location', 'latitude', 'longitude', 
			'date', 'time', 'date_to', 'time_to',  
			'registration', 'banner',)
		labels = {'date': '', 'time': '', 'date_to': '', 'time_to': '',}
		widgets = {
			'title': forms.TextInput(attrs={ 'readonly': 'True'},),
			'location': forms.TextInput(attrs={ 'readonly': 'True'},),
			'description': forms.Textarea(attrs={ 'readonly': 'True'},),
			'meetup_ID': forms.TextInput(attrs={'readonly': 'readonly', 'readonly': 'True'},),
			'date': forms.DateInput(attrs={'type': 'date', 'readonly': 'True'},),
			'time': forms.TimeInput(attrs={'type': 'time', 'readonly': 'True'},),
			'date_to': forms.DateInput(attrs={'type': 'date', 'readonly': 'True'},),
			'time_to': forms.TimeInput(attrs={'type': 'time', 'readonly': 'True'},),
			'latitude': forms.TextInput(attrs={'hidden': 'True', 'readonly': 'True'}),
			'longitude': forms.TextInput(attrs={'hidden': 'True', 'readonly': 'True'}),}
		help_texts ={'registration': '*Complete event registration URL',}

	def clean_banner(self):
		return self.cleaned_data['banner'] or None


class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ('name', 'feedback',)


class EventStatisticForm(forms.ModelForm):
	class Meta:
		model = EventStatistics
		fields = ('male', 'female',)


class EventStatisticManualCountForm(forms.ModelForm):
	class Meta:
		model = EventStatistics
		fields = ('manual_count',)


class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = ('banner', 'title', 'description',)

	def clean_banner(self):
		return self.cleaned_data['banner'] or None