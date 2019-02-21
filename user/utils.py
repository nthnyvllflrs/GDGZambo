import random, string

from django.utils.text import slugify

DONT_USE = ['create', 'list',]
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		try: slug = slugify(instance.title)
		except: slug = slugify(instance.name)

	if slug in DONT_USE:
		new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
		return unique_slug_generator(instance, new_slug=new_slug)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug=slug).exists()
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
		slug=slug,
		randstr=random_string_generator(size=4)
		)
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug


from django.conf import settings
from django.core.mail import send_mail 


def sndml(subject=None, body=None, recipients_list=()):
	email_subject = subject
	email_body = body
	recipients_list = recipients_list
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, recipients_list)


def send_event_notification(instance):
	subscriber_list = [ (subscriber.user.email) for subscriber in Subscriber.objects.filter(events=True)]
	recipients_list = tuple(subscriber_list)

	subject = 'New GDG Zamboanga Event <%s>' % (instance.title,)
	body = instance.description[:200]
	sndml(subject, body, recipients_list)


def send_blog_notification(instance):
	subscriber_list = [ (subscriber.user.email) for subscriber in Subscriber.objects.filter(blogs=True)]
	recipients_list = tuple(subscriber_list)

	subject = 'New GDG Zamboanga Blog <%s>' % (instance.title,)
	body = instance.body[:200]
	sndml(subject, body, recipients_list)


def send_story_notification(instance):
	subscriber_list = [ (subscriber.user.email) for subscriber in Subscriber.objects.filter(stories=True)]
	recipients_list = tuple(subscriber_list)

	subject = 'New GDG Zamboanga Story <%s>' % (instance.title,)
	body = instance.body[:200]
	sndml(subject, body, recipients_list)


def send_welcome_email(instance):
	subject = "Welcome To GDG Zamboanga"
	body = """
		Dear %s,

		Thank you for subscribing to GDG Zamboanga!

		Sincerly,
		GDG Zamboanga
		""" % (instance.name)
	email = instance.email
	sndml(subject, body, (email,))