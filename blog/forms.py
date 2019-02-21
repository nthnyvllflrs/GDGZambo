# Django imports
from django import forms

# Inner App imports
from .models import (Blog, Photo, Comment,)

class BlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ('title', 'body', 'video_url',)
		widgets = {'video_url': forms.TextInput(attrs={'placeholder': 'https://www.youtube.com/embed/OREP8HGsTpM'},),}
		help_texts ={'video_url': '*Enter a valid youtube video url',}


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ('image',)

	def clean_image(self):
		return self.cleaned_data['image'] or None


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','comment',)