# Django imports
from django.db import models
from django.db.models.signals import pre_save

# Import CloudinaryField for image 
from cloudinary.models import CloudinaryField

from .utils import unique_slug_generator

class Member(models.Model):
	photo = CloudinaryField('photo', blank=True, null=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	name = models.CharField(max_length=120)
	position = models.CharField(max_length=120)
	description = models.TextField()
	expertise = models.TextField(null=True, blank=True)
	email = models.EmailField()
	facebook = models.CharField(max_length=500, null=True, blank=True)
	twitter = models.CharField(max_length=500, null=True, blank=True)
	instagram = models.CharField(max_length=500, null=True, blank=True)
	website = models.URLField(max_length=500, null=True, blank=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

def member_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	# if instance.facebook:
	# 	instance.facebook = 'https://www.facebook.com/' + instance.facebook
	# if instance.twitter:
	# 	instance.twitter = 'https://www.twitter.com/' + instance.twitter
	# if instance.instagram:
	# 	instance.instagram = 'https://www.instagram.com/' + instance.instagram
pre_save.connect(member_pre_save_receiver, sender=Member)


class Volunteer(models.Model):
	name = models.CharField(max_length=200)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	photo = CloudinaryField('photo', blank=True, null=True)
	description = models.TextField(max_length=300)
	expertise = models.TextField(null=True, blank=True)
	email = models.EmailField()
	facebook = models.CharField(max_length=500, null=True, blank=True)
	twitter = models.CharField(max_length=500, null=True, blank=True)
	instagram = models.CharField(max_length=500, null=True, blank=True)
	website = models.URLField(max_length=500, null=True, blank=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

def volunteer_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	# if instance.facebook:
	# 	instance.facebook = 'https://www.facebook.com/' + instance.facebook
	# if instance.twitter:
	# 	instance.twitter = 'https://www.twitter.com/' + instance.twitter
	# if instance.instagram:
	# 	instance.instagram = 'https://www.instagram.com/' + instance.instagram
pre_save.connect(volunteer_pre_save_receiver, sender=Volunteer)