# Django imports
from django import forms

# Inner App imports
from .models import Story, Image


class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = ('title', 'body', 'video_url',)
		widgets = {'video_url': forms.TextInput(attrs={'placeholder': 'https://youtu.be/OREP8HGsTpM'},),}
		help_texts ={'video_url': '*Enter a valid youtube video url',}


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('photo',)

	def clean_photo(self):
		return self.cleaned_data['photo'] or None