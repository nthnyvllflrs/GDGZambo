# Django imports
from django import form

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
			'facebook': forms.URLInput(attrs={'id': 'sponsor-facebook',}),
			'twitter': forms.URLInput(attrs={'id': 'sponsor-twitter',}),
			'instagram': forms.URLInput(attrs={'id': 'sponsor-instagram',}),
			'website': forms.URLInput(attrs={'id': 'sponsor-website',}),}

	def clean_photo(self):
		return self.cleaned_data['photo'] or None


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
			'facebook': forms.URLInput(attrs={'id': 'speaker-facebook',}),
			'twitter': forms.URLInput(attrs={'id': 'speaker-twitter',}),
			'instagram': forms.URLInput(attrs={'id': 'speaker-instagram',}),
			'website': forms.URLInput(attrs={'id': 'speaker-website',}),
		}

	def clean_photo(self):
		return self.cleaned_data['photo'] or None


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
			'title': forms.TextInput(attrs={'readonly': 'readonly'},),
			'location': forms.TextInput(attrs={'readonly': 'readonly'},),
			'description': forms.Textarea(attrs={'readonly': 'readonly'},),
			'meetup_ID': forms.TextInput(attrs={'readonly': 'readonly'},),
			'date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
			'time': forms.TimeInput(attrs={'type': 'time', 'readonly': 'readonly'}),
			'date_to': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
			'time_to': forms.TimeInput(attrs={'type': 'time','readonly': 'readonly'}),
			'latitude': forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'hidden'}),
			'longitude': forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'hidden'}),}
		help_texts ={'registration': '*Complete event registration URL',}

	def clean_meetup_ID(self):
    meetup_ID = self.cleaned_data.get('meetup_ID')
    try:
    	meetup_event = settings.MEETUP_CLIENT.GetEvent({'id': meetup_ID})
    except:
    	raise forms.ValidationError("Meetup ID is invalid.")
    return meetup_ID

	def clean_banner(self):
		return self.cleaned_data['banner'] or None


class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ('name', 'feedback',)


class EventStatisticForm(forms.ModelForm):
	class Meta:
		model = EventStatistic
		fields = ('male', 'female',)


class EventStatisticManualCountForm(forms.ModelForm):
	class Meta:
		model = EventStatistic
		fields = ('manual_count',)


class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = ('banner', 'title', 'description',)

	def clean_banner(self):
		return self.cleaned_data['banner'] or None