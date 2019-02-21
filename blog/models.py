# Django imports
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

# Import CloudinaryField for image 
from cloudinary.models import CloudinaryField

# Inner App imports
from .utils import unique_slug_generator


class Blog(models.Model):
	title 		= models.CharField(max_length=120)
	author 		= models.ForeignKey(User, on_delete=models.CASCADE)
	body 			= models.TextField()
	video_url = models.URLField(max_length=500, blank=True, null=True)
	status 		= models.CharField(max_length=120, default='Draft')
	slug 			= models.SlugField(null=True, blank=True)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

def __str__(self):
	return self.title

def blog_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
pre_save.connect(blog_pre_save_receiver, sender=Blog)


class Photo(models.Model):
	blog 		= models.ForeignKey('Blog', on_delete=models.CASCADE)
	image 	= CloudinaryField('photo')

	def __str__(self):
		return self.blog.title


class Comment(models.Model):
	blog 			= models.ForeignKey('Blog', on_delete=models.CASCADE)
	name 			= models.CharField(max_length=120, default="Anonymous", blank=True, null=True)
	comment 	= models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name