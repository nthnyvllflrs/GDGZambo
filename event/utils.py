import random, string

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.text import slugify


DONT_USE = ['create', 'speaker', 'upcoming', 'past', 'info', 'draft-save', 'rsvp', 'sponsor', 'statistics']
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


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail 
from django.template import loader
from django.shortcuts import get_object_or_404


def send_event_notification_to_speakers(instance):
	print("SENDING EMAIL!")
	speaker_email_list = [(speaker.email) for speaker in instance.speakers.all()]
	member_speaker_email_list = [(speaker.email) for speaker in instance.member_speaker.all()]
	speaker_emails = speaker_email_list + member_speaker_email_list
	speaker_emails = [email for email in speaker_emails if not(email == None)]

	email_subject = '(GDG Zamboanga Speaker) New GDG Zamboanga Event <%s>' % (instance.title,)
	email_body = '' 
	email_from = settings.EMAIL_HOST_USER
	recipient_list = tuple(speaker_emails)
	html_message = loader.render_to_string('email/subscriber-event-notification-speaker.html',{'event': instance})
	send_mail(email_subject, email_body, email_from, recipient_list, html_message=html_message)


def send_event_notification_to_speakers_updated(instance):
	print("SENDING EMAIL UPDATED!")
	speaker_email_list = [(speaker.email) for speaker in instance.speakers.all()]
	member_speaker_email_list = [(speaker.email) for speaker in instance.member_speaker.all()]
	speaker_emails = speaker_email_list + member_speaker_email_list
	speaker_emails = [email for email in speaker_emails if not(email == None)]

	email_subject = '(GDG Zamboanga Speaker) Updated GDG Zamboanga Event <%s>' % (instance.title,)
	email_body = '' 
	email_from = settings.EMAIL_HOST_USER
	recipient_list = tuple(speaker_emails)
	html_message = loader.render_to_string('email/subscriber-event-notification-speaker-updated.html',{'event': instance})
	send_mail(email_subject, email_body, email_from, recipient_list, html_message=html_message)