from django import forms

from .models import Member, Volunteer

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = (
			'photo', 'firstname', 'lastname', 'email', 'description', 'position',
			'expertise', 'facebook', 'twitter', 'instagram', 'website',
		)

		widgets = {
			'description': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'member-description',}),
			'expertise': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'member-expertise',}),
			'facebook': forms.URLInput(attrs={'id': 'member-facebook',}),
			'twitter': forms.URLInput(attrs={'id': 'member-twitter',}),
			'instagram': forms.URLInput(attrs={'id': 'member-instagram',}),
			'website': forms.URLInput(attrs={'id': 'member-website',}),
		}

	def clean_photo(self):
		return self.cleaned_data['photo'] or None


class VolunteerForm(forms.ModelForm):
	class Meta:
		model = Volunteer
		fields = (
			'photo', 'firstname', 'lastname', 'email', 'description',
			'expertise', 'facebook', 'twitter', 'instagram', 'website',
		)
		widgets = {
		'firstname': forms.TextInput(attrs={'id': 'volunteer-firstname'}),
		'lastname': forms.TextInput(attrs={'id': 'volunteer-lastname'}),
		'email': forms.EmailInput(attrs={'id': 'volunteer-email'}),
		'description': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'volunteer-description',}),
		'expertise': forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'volunteer-expertise',}),
		'facebook': forms.URLInput(attrs={'id': 'volunteer-facebook',}),
		'twitter': forms.URLInput(attrs={'id': 'volunteer-twitter',}),
		'instagram': forms.URLInput(attrs={'id': 'volunteer-instagram',}),
		'website': forms.URLInput(attrs={'id': 'volunteer-website',}),}

	def clean_photo(self):
		return self.cleaned_data['photo'] or None