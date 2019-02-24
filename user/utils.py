from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail 
from django.template import loader
from django.shortcuts import get_object_or_404

from .models import Subscriber, UserAccount


def send_event_notification(instance):
	email_subject = 'New GDG Zamboanga Event <%s>' % (instance.title,)
	email_body = '' 
	email_from = settings.EMAIL_HOST_USER
	subscriber_list = [ (subscriber.email) for subscriber in Subscriber.objects.all()]
	recipient_list = tuple(subscriber_list)
	html_message = loader.render_to_string('email/subscriber-event-notification.html',{'event': instance})
	send_mail(email_subject, email_body, email_from, recipient_list, html_message=html_message)


def send_blog_notification(instance):
	email_subject = 'New GDG Zamboanga Blog <%s>' % (instance.title,)
	email_body = '' 
	email_from = settings.EMAIL_HOST_USER
	subscriber_list = [ (subscriber.email) for subscriber in Subscriber.objects.all()]
	recipient_list = tuple(subscriber_list)
	html_message = loader.render_to_string('email/subscriber-blog-notification.html',{'blog': instance})
	send_mail(email_subject, email_body, email_from, recipient_list, html_message=html_message)


def send_story_notification(instance):
	email_subject = 'New GDG Zamboanga Story <%s>' % (instance.title,)
	email_body = '' 
	email_from = settings.EMAIL_HOST_USER
	subscriber_list = [ (subscriber.email) for subscriber in Subscriber.objects.all()]
	recipient_list = tuple(subscriber_list)
	html_message = loader.render_to_string('email/subscriber-story-notification.html',{'story': instance})
	send_mail(email_subject, email_body, email_from, recipient_list, html_message=html_message)


def send_welcome_email(instance):
	email_subject = "Welcome To GDG Zamboanga"
	email_body = ''
	html_message = loader.render_to_string('email/subscription.html',{'subscriber': instance})
	recipient_list = instance.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)


def send_removed_email(instance):
	email_subject = "Removed by GDG Zamboanga Administrator"
	email_body = ''
	html_message = loader.render_to_string('email/removed-notification.html',{'subscriber': instance})
	recipient_list = instance.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)


def send_goodbye_email(instance):
	email_subject = "Goodbye From GDG Zamboanga"
	email_body = ''
	html_message = loader.render_to_string('email/goodbye-notification.html',{'subscriber': instance})
	recipient_list = instance.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)


def send_blog_published_notification(member, instance):
	email_subject = "%s is now published." % (instance.title)
	email_body = ''
	html_message = loader.render_to_string('email/published-blog-notification.html',{'instance': instance})
	recipient_list = member.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)


def send_story_published_notification(member, instance):
	email_subject = "%s is now published." % (instance.title)
	email_body = ''
	html_message = loader.render_to_string('email/published-story-notification.html',{'instance': instance})
	recipient_list = member.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)


def send_comment_notification(instance):
	email_subject = "New Comment <%s>" % (instance.blog.title)
	email_body = ''
	html_message = loader.render_to_string('email/comment-notification.html',{'instance': instance})
	recipient_list = instance.blog.author.useraccount.member.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)


def send_feedback_notification(instance):
	email_subject = "New Feedback <%s>" % (instance.event.title)
	email_body = ''
	html_message = loader.render_to_string('email/feedback-notification.html',{'instance': instance})
	recipient_list = instance.event.author.useraccount.member.email
	email_from = settings.EMAIL_HOST_USER
	send_mail(email_subject, email_body, email_from, (recipient_list,), html_message=html_message)