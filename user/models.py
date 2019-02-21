# Django imports
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

# Import CloudinaryField for image 
from cloudinary.models import CloudinaryField

# Inner App imports
from .utils import unique_slug_generator

class Member(models.Model):
	photo 			= CloudinaryField('photo', blank=True, null=True)
	firstname 	= models.CharField(max_length=100)
	lastname 		= models.CharField(max_length=100)
	name 				= models.CharField(max_length=120)
	description = models.TextField()
	expertise 	= models.TextField(null=True, blank=True)
	email 			= models.EmailField(null=True, blank=True)
	facebook 		= models.URLField(max_length=500, null=True, blank=True)
	twitter 		= models.URLField(max_length=500, null=True, blank=True)
	instagram 	= models.URLField(max_length=500, null=True, blank=True)
	website 		= models.URLField(max_length=500, null=True, blank=True)
	slug 				= models.SlugField(null=True, blank=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

def member_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
pre_save.connect(member_pre_save_receiver, sender=Member)


class Subscriber(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	events = models.BooleanField(default=True)
	blogs = models.BooleanField(default=True)
	stories = models.BooleanField(default=True)

	def __str__(self):
		return self.user.email


class UserAccount(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	member 		= models.OneToOneField(Member, on_delete=models.CASCADE)
	role 			= models.CharField(max_length=120, default='Blog Creator')
	activated = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	@property
	def is_blog_creator(self):
		return True if (str(self.role) == 'Blog Creator') else False

	@property
	def is_event_creator(self):
		return True if (str(self.role) == 'Event Creator') else False


class UserLog(models.Model):
	user 				= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	description = models.TextField()
	timestamp 	= models.DateTimeField(auto_now_add=True, auto_now=False)


class SiteCarousel(models.Model):
	image = CloudinaryField('image', blank=True, null=True)


class DynamicData(models.Model):
	become_a_sponsor_url = models.URLField(max_length=1000, default='https://gdgzamboanga.herokuapp.com/')
	become_a_volunteer_url = models.URLField(max_length=1000, default='https://gdgzamboanga.herokuapp.com/')
	speaker_request_url = models.URLField(max_length=1000, default='https://gdgzamboanga.herokuapp.com/')
	media_kit_url = models.URLField(max_length=1000, default='https://gdgzamboanga.herokuapp.com/')
	photo_gallery_url = models.URLField(max_length=1000, default='https://gdgzamboanga.herokuapp.com/')

	about_us = models.TextField(default="GDG Zamboanga")

	google_plus_link = models.URLField(max_length=300, default='https://plus.google.com/')
	facebook_link = models.URLField(max_length=300, default='https://facebook.com/')
	twitter_link = models.URLField(max_length=300, default='https://twitter.com')
	youtube_link = models.URLField(max_length=300, default='https://youtube.com')
	instagram_link = models.URLField(max_length=300, default='https://instagram.com')
	meetup_link = models.URLField(max_length=300, default='https://meetup.com')