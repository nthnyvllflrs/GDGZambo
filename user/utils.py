from django.conf import settings
from django.core.mail import send_mail 
from .models import Subscriber

def sndml(subject=None, body=None, recipients_list=()):
	email_subject = subject
	email_body = body
	recipients_list = recipients_list
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, recipients_list)


def send_event_notification(instance):
	subscriber_list = [ (subscriber.email) for subscriber in Subscriber.objects.all()]
	recipients_list = tuple(subscriber_list)

	subject = 'New GDG Zamboanga Event <%s>' % (instance.title,)
	body = instance.description[:200] + '... Read full event details here https://gdgzambo.herokuapp.com/event/' + instance.slug 
	sndml(subject, body, recipients_list)


def send_blog_notification(instance):
	subscriber_list = [ (subscriber.email) for subscriber in Subscriber.objects.all()]
	recipients_list = tuple(subscriber_list)

	subject = 'New GDG Zamboanga Blog <%s>' % (instance.title,)
	body = instance.body[:200] + '... Read the full blog details here https://gdgzambo.herokuapp.com/blog/' + instance.slug 
	sndml(subject, body, recipients_list)


def send_story_notification(instance):
	subscriber_list = [ (subscriber.email) for subscriber in Subscriber.objects.all()]
	recipients_list = tuple(subscriber_list)

	subject = 'New GDG Zamboanga Story <%s>' % (instance.title,)
	body = instance.body[:200] + '... Read full story here details https://gdgzambo.herokuapp.com/story/' + instance.slug 
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