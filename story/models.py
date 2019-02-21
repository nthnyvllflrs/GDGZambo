# Django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

# Import CloudinaryField for image 
from cloudinary.models import CloudinaryField

# Inner App imports
from .utils import unique_slug_generator


class Story(models.Model):
	title 		= models.CharField(max_length=120)
	author 		= models.ForeignKey(User, on_delete=models.CASCADE)
	body 			= models.TextField()
	video_url = models.URLField(max_length=500, blank=True, null=True)
	slug 			= models.SlugField(null=True, blank=True)
	status 		= models.CharField(max_length=120, default='Draft')
	updated 	= models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

def story_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
pre_save.connect(story_pre_save_receiver, sender=Story)


class Image(models.Model):
	story = models.ForeignKey('Story', on_delete=models.CASCADE)
	photo = CloudinaryField('photo')

	def __str__(self):
		return self.story.title