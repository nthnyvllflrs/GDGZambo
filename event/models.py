# Django imports
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

# Import CloudinaryField for image 
from cloudinary.models import CloudinaryField

# Inner App imports
from .utils import unique_slug_generator

# Outer App imports
from team.models import Member, Volunteer


def volunteer_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
pre_save.connect(volunteer_pre_save_receiver, sender=Volunteer)


class Sponsor(models.Model):
	name = models.CharField(max_length=200)
	photo = CloudinaryField('photo', blank=True, null=True)
	description = models.CharField(max_length=300)
	email = models.EmailField(null=True, blank=True)
	facebook = models.CharField(max_length=500, null=True, blank=True)
	twitter = models.CharField(max_length=500, null=True, blank=True)
	instagram = models.CharField(max_length=500, null=True, blank=True)
	website = models.URLField(max_length=500, null=True, blank=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

def sponsor_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	# if instance.facebook:
	# 	instance.facebook = 'https://www.facebook.com/' + instance.facebook
	# if instance.twitter:
	# 	instance.twitter = 'https://www.twitter.com/' + instance.twitter
	# if instance.instagram:
	# 	instance.instagram = 'https://www.instagram.com/' + instance.instagram
pre_save.connect(sponsor_pre_save_receiver, sender=Sponsor)

class Speaker(models.Model):
	name = models.CharField(max_length=200)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	photo = CloudinaryField('photo', blank=True, null=True)
	description = models.TextField(max_length=300)
	expertise = models.TextField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	facebook = models.CharField(max_length=500, null=True, blank=True)
	twitter = models.CharField(max_length=500, null=True, blank=True)
	instagram = models.CharField(max_length=500, null=True, blank=True)
	website = models.URLField(max_length=500, null=True, blank=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

def speaker_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	# if instance.facebook:
	# 	instance.facebook = 'https://www.facebook.com/' + instance.facebook
	# if instance.twitter:
	# 	instance.twitter = 'https://www.twitter.com/' + instance.twitter
	# if instance.instagram:
	# 	instance.instagram = 'https://www.instagram.com/' + instance.instagram
pre_save.connect(speaker_pre_save_receiver, sender=Speaker)


class Event(models.Model):
	meetup_ID = models.CharField(max_length=120)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=120)
	description	= models.TextField()
	banner = CloudinaryField('banner', blank=True, null=True)

	location = models.CharField(max_length=200)
	latitude = models.CharField(max_length=200, default=6.9214)
	longitude = models.CharField(max_length=200, default=122.0790)

	date = models.DateField(auto_now=False, auto_now_add=False)
	time = models.TimeField(auto_now=False, auto_now_add=False)
	date_to = models.DateField(auto_now=False, auto_now_add=False)
	time_to = models.TimeField(auto_now=False, auto_now_add=False)

	speakers = models.ManyToManyField(Speaker, blank=True)
	sponsors = models.ManyToManyField(Sponsor, blank=True)
	volunteers = models.ManyToManyField(Volunteer)
	member_speaker = models.ManyToManyField(Member)
	member_sponsor = models.ManyToManyField(Member, related_name='sponsored_events')
	member_volunteer = models.ManyToManyField(Member, related_name='volunteered_events')

	registration = models.URLField(max_length=1000, blank=True, null=True)
	status = models.CharField(max_length=120, default='Draft')

	slug = models.SlugField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	@property
	def is_past_event(self):
		return date.today() > self.date_to

	@property
	def event_status(self):
		if self.date <= date.today() <= self.date_to:
			return 'Ongoing'
		elif date.today() > self.date_to:
			return 'Past'
		else:
			return 'Upcoming'

	@property
	def attendees(self):
		meetup_event = settings.MEETUP_CLIENT.GetEvent({'id': self.meetup_ID})
		return meetup_event.yes_rsvp_count

def event_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
pre_save.connect(event_pre_save_receiver, sender=Event)


class Feedback(models.Model):
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	name = models.CharField(max_length=120, default="Anonymous", blank=True, null=True)
	feedback = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class EventStatistics(models.Model):
	event = models.OneToOneField(Event, on_delete=models.CASCADE)
	male = models.IntegerField(default=0)
	female = models.IntegerField(default=0)
	yes_rsvp = models.IntegerField(default=0)
	no_rsvp = models.IntegerField(default=0)
	manual_count = models.IntegerField(default=0)

	def __str__(self):
		return self.event.title


class EventAttendance(models.Model):
	event_statistic = models.ForeignKey(EventStatistics, on_delete=models.CASCADE)
	member_id = models.CharField(max_length=100)
	member_name = models.CharField(max_length=300)
	member_image = models.URLField(max_length=300, blank=True, null=True)

	def __str__(self):
		return self.member_name


class Info(models.Model):
	banner 	= CloudinaryField('banner', blank=True, null=True)
	title = models.CharField(max_length=120)
	description = models.TextField()
	slug = models.SlugField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

def info_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
pre_save.connect(info_pre_save_receiver, sender=Info)