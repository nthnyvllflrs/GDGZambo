import datetime
import json
import threading
import cloudinary
from bs4 import BeautifulSoup

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import (Sponsor, Speaker, Event, Feedback, EventStatistics, EventAttendance, Info,)
from .forms import (SponsorForm, SpeakerForm, EventForm, FeedbackForm, EventStatisticForm, EventStatisticManualCountForm)
from .utils import render_to_pdf

from user.models import UserLog
from user.utils import send_event_notification, send_feedback_notification, send_event_updated_notification
from team.models import Member, Volunteer
from team.forms import VolunteerForm

def list_speaker(request):
	form = SpeakerForm()
	speaker_list = Speaker.objects.order_by('firstname', 'lastname')
	context = {'form': form,'speaker_list': speaker_list,}
	return render(request, 'event/speaker-list.html', context)


@login_required
def create_speaker(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	if request.method == 'POST':
		speaker_form = SpeakerForm(request.POST, request.FILES)
		if speaker_form.is_valid():
			speaker = speaker_form.save(commit=False)
			speaker.name = speaker_form.cleaned_data['firstname'] + ' ' + speaker_form.cleaned_data['lastname']
			speaker.save()
			UserLog.objects.create(user = request.user, description = "New Speaker Created. (%s)" % (speaker.name,),)
			return redirect('event:speaker-list')
	else:
		speaker_form = SpeakerForm()
	context = {'speaker_form': speaker_form}
	return render(request, 'event/speaker-create.html', context)


@login_required
def update_speaker(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	speaker = get_object_or_404(Speaker, slug=slug)
	if request.method == 'POST':
		speaker_form = SpeakerForm(request.POST, request.FILES, instance=speaker)
		if speaker_form.is_valid():
			speaker = speaker_form.save(commit=False)
			speaker.name = speaker_form.cleaned_data['firstname'] + ' ' + speaker_form.cleaned_data['lastname']
			speaker.save()
			UserLog.objects.create(user = request.user, description = "Speaker Updated. (%s)" % (speaker.name,),)
			return redirect('event:speaker-list')
	else:
		speaker_form = SpeakerForm(instance=speaker)
	context = {'speaker': speaker, 'speaker_form': speaker_form}
	return render(request, 'event/speaker-update.html', context)


@login_required
def delete_speaker(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	speaker = get_object_or_404(Speaker, slug=slug)
	UserLog.objects.create(user = request.user, description = "Speaker Removed. (%s)" % (speaker.name,),)
	speaker.delete()
	return redirect('event:speaker-list')


def list_sponsor(request):
	sponsor_list = Sponsor.objects.order_by('name')
	context = {'sponsor_list': sponsor_list,}
	return render(request, 'event/sponsor-list.html', context)


@login_required
def create_sponsor(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	if request.method == 'POST':
		sponsor_form = SponsorForm(request.POST, request.FILES)
		if sponsor_form.is_valid():
			sponsor = sponsor_form.save(commit=False)
			sponsor.save()
			UserLog.objects.create(user = request.user, description = "New Sponsor Created. (%s)" % (sponsor.name,),)
			return redirect('event:sponsor-list')
	else:
		sponsor_form = SponsorForm()
	context = {'sponsor_form': sponsor_form}
	return render(request, 'event/sponsor-create.html', context)


@login_required
def update_sponsor(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	sponsor = get_object_or_404(Sponsor, slug=slug)
	if request.method == 'POST':
		sponsor_form = SponsorForm(request.POST, request.FILES, instance=sponsor)
		if sponsor_form.is_valid():
			sponsor = sponsor_form.save(commit=False)
			sponsor.save()
			UserLog.objects.create(user = request.user, description = "Sponsor Updated. (%s)" % (sponsor.name,),)
			return redirect('event:sponsor-list')
	else:
		sponsor_form = SponsorForm(instance=sponsor)
	context = {'sponsor': sponsor, 'sponsor_form': sponsor_form}
	return render(request, 'event/sponsor-update.html', context)


@login_required
def delete_sponsor(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	sponsor = get_object_or_404(Sponsor, slug=slug)
	UserLog.objects.create(user = request.user, description = "Sponsor Removed. (%s)" % (sponsor.name,),)
	sponsor.delete()
	return redirect('event:sponsor-list')


def view_event(request, slug):
	event = get_object_or_404(Event, slug=slug)
	if event.status != 'Publish' and not request.user.is_authenticated:
		return redirect('landing-page')
	context = {'event': event,}
	return render(request, 'event/event-view.html', context)


def list_upcoming_events(request):
	date_now = datetime.datetime.now().date()
	e_event = Event.objects.filter(Q(date__lte=date_now) & Q(date_to__gte=date_now) & Q(status='Publish'))
	event_list = Event.objects.filter(date__gt=date_now, status='Publish').order_by('date')
	context = {'e_event': e_event, 'event_list': event_list,}
	return render(request, 'event/event-upcoming.html', context)


def list_past_events(request):
	date_now = datetime.datetime.now().date()
	event_list = Event.objects.filter(date_to__lt=date_now, status='Publish').order_by('-date')
	context = {'event_list': event_list,}
	return render(request, 'event/event-past.html', context)


@login_required
def create_pre_event(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	error = None
	if request.method == 'POST':
		if request.POST['meetupId']:
			try:
				meetup_id = request.POST['meetupId']
				meetup_event = settings.MEETUP_CLIENT.GetEvent({'id': meetup_id})
				return redirect('event:event-create', meetup_id=meetup_id)
			except Exception as e:
				error = 'Invalid Meetup ID. Please enter a valid Event Meetup ID to proceed.'
	context = {'error': error,}
	return render(request, 'event/event-pre-create.html', context)


@login_required
def create_event(request, meetup_id):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	photo_url = None
	if request.method == 'POST':
		event_status = 'Draft' if('Draft' in request.POST) else 'Publish'
		speakers = request.POST.getlist('speakers')
		sponsors = request.POST.getlist('sponsors')
		volunteers = request.POST.getlist('volunteers')
		member_speakers = request.POST.getlist('member_speakers')
		member_sponsors = request.POST.getlist('member_sponsors')
		member_volunteers = request.POST.getlist('member_volunteers')

		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			event = form.save(commit=False)
			event.author = request.user
			event.status = event_status
			event.save()

			if speakers:
				for speaker in speakers:
					event.speakers.add(Speaker.objects.get(pk=speaker))

			if sponsors:
				for sponsor in sponsors:
					event.sponsors.add(Sponsor.objects.get(pk=sponsor))

			if member_speakers:
				for member in member_speakers:
					event.member_speaker.add(Member.objects.get(pk=member))

			if member_sponsors:
				for member in member_sponsors:
					event.member_sponsor.add(Member.objects.get(pk=member))

			if volunteers:
				for volunteer in volunteers:
					event.volunteers.add(Volunteer.objects.get(pk=volunteer))

			if member_volunteers:
				for volunteer in member_volunteers:
					event.member_volunteer.add(Member.objects.get(pk=volunteer))

			if not ('overwrite' in request.POST) and 'meetup_photo_url' in request.POST:
				if request.POST['meetup_photo_url'] != 'None':
					meetup_photo_url = request.POST['meetup_photo_url']
					meetup_banner = cloudinary.uploader.upload(meetup_photo_url)
					result = cloudinary.CloudinaryResource(public_id=meetup_banner['public_id'], type=meetup_banner['type'], 
						resource_type=meetup_banner['resource_type'], version=meetup_banner['version'], format=meetup_banner['format'])
					str_result = result.get_prep_value()
					event.banner = str_result
			event.save()

			EventStatistics.objects.create(event=event)
			UserLog.objects.create(user = request.user, description = "New Event Created. (%s)" % (event.title,),)
			if ('Yes' in request.POST) and event.status == 'Publish':
				t = threading.Thread(target=send_event_notification(event))
				t.setDaemon = True
				t.start()
			return redirect('event:event-upcoming')
	else:
		meetup_event = settings.MEETUP_CLIENT.GetEvent({'id': meetup_id})

		# Get Event Banner
		photo_url = meetup_event.photo_url if 'photo_url' in meetup_event.__dict__ else None

		if 'venue' in meetup_event.__dict__:
			venue_name = meetup_event.venue['name'] if 'name' in meetup_event.venue else ''
			address_1 = meetup_event.venue['address_1'] if 'address_1' in meetup_event.venue else ''
			address_2 = meetup_event.venue['address_2'] if 'address_2' in meetup_event.venue else ''
			city = meetup_event.venue['city'] if 'city' in meetup_event.venue else ''
			event_lat = meetup_event.venue['lat'] if 'lat' in meetup_event.venue else 6.9214
			event_lng = meetup_event.venue['lon'] if 'lon' in meetup_event.venue else 122.0790
			event_location = venue_name + ', ' + address_1 + ', ' + address_2 + ', ' +  city
		else:
			event_location = 'No event venue was set'
			event_lat = 6.9214
			event_lng = 122.0790
		# Get Event Duration
		event_duration = meetup_event.duration if 'duration' in  meetup_event.__dict__ else 0
		# Get Event Description
		event_description = meetup_event.description if 'description' in  meetup_event.__dict__ else 'No Description'

		event_start = datetime.datetime.fromtimestamp(meetup_event.time/1000.0)
		event_start_date = event_start.strftime("%Y-%m-%d")
		event_start_time = event_start.strftime("%H:%M:%S")
		event_end = datetime.datetime.fromtimestamp(meetup_event.time/1000.0) + datetime.timedelta(hours=event_duration/3600000)
		event_end_date = event_end.strftime("%Y-%m-%d")
		event_end_time = event_end.strftime("%H:%M:%S")

		event_description = BeautifulSoup(event_description, features='html.parser').get_text(separator='\n')

		form = EventForm(initial={
			'author': request.user, 'title': meetup_event.name, 'location': event_location, 'latitude': event_lat,
			'longitude': event_lng, 'date': event_start_date, 'time': event_start_time, 'date_to': event_end_date,
			'time_to': event_end_time, 'description': event_description, 'meetup_ID': meetup_id,})

	speaker_form = SpeakerForm()
	sponsor_form = SponsorForm()
	volunteer_form = VolunteerForm()

	speaker_list = Speaker.objects.all()
	sponsor_list = Sponsor.objects.all()
	member_list = Member.objects.all()
	volunteer_list = Volunteer.objects.all()

	context = {
		'form': form, 'speaker_form': speaker_form, 'sponsor_form': sponsor_form, 'volunteer_form': volunteer_form, 'speaker_list': speaker_list, 
		'sponsor_list': sponsor_list, 'member_list': member_list, 'volunteer_list': volunteer_list, 'photo_url': photo_url, 
		'start_date': event_start_date, 'end_date': event_end_date}
	return render(request, 'event/event-create.html', context)


@login_required
def update_event(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	event = get_object_or_404(Event, slug=slug)
	meetup_id = event.meetup_ID
	if request.method == 'POST':
		event_form = EventForm(request.POST, request.FILES, instance=event)
		if event_form.is_valid():
			event = event_form.save(commit=False)

			event_speakers = request.POST.getlist('checked_speakers')
			unchecked_speakers = event.speakers.exclude(id__in=event_speakers)
			checked_speakers = request.POST.getlist('unchecked_speakers')

			event_sponsors = request.POST.getlist('checked_sponsors')
			unchecked_sponsors = event.sponsors.exclude(id__in=event_sponsors)
			checked_sponsors = request.POST.getlist('unchecked_sponsors')

			event_volunteers = request.POST.getlist('checked_volunteers')
			unchecked_volunteers = event.volunteers.exclude(id__in=event_volunteers)
			checked_volunteers = request.POST.getlist('unchecked_volunteers')

			event_member_speakers = request.POST.getlist('checked_member_speakers')
			unchecked_member_speakers = event.member_speaker.exclude(id__in=event_member_speakers)
			checked_member_speakers = request.POST.getlist('unchecked_member_speakers')

			event_member_sponsors = request.POST.getlist('checked_member_sponsors')
			unchecked_member_sponsors = event.member_sponsor.exclude(id__in=event_member_sponsors)
			checked_member_sponsors = request.POST.getlist('unchecked_member_sponsors')

			event_member_volunteers = request.POST.getlist('checked_member_volunteers')
			unchecked_member_volunteers = event.member_volunteer.exclude(id__in=event_member_volunteers)
			checked_member_volunteers = request.POST.getlist('unchecked_member_volunteers')
			
			if unchecked_speakers:
				for speaker in unchecked_speakers:
					event.speakers.remove(speaker)
			if checked_speakers:
				for speaker in checked_speakers:
					event.speakers.add(Speaker.objects.get(pk=speaker))

			if unchecked_sponsors:
				for sponsor in unchecked_sponsors:
					event.sponsors.remove(sponsor)
			if checked_sponsors:
				for sponsor in checked_sponsors:
					event.sponsors.add(Sponsor.objects.get(pk=sponsor))

			if unchecked_volunteers:
				for volunteer in unchecked_volunteers:
					event.volunteers.remove(volunteer)
			if checked_volunteers:
				for volunteer in checked_volunteers:
					event.volunteers.add(Volunteer.objects.get(pk=volunteer))

			if unchecked_member_speakers:
				for member in unchecked_member_speakers:
					event.member_speaker.remove(member)
			if checked_member_speakers:
				for member in checked_member_speakers:
					event.member_speaker.add(Member.objects.get(pk=member))

			if unchecked_member_sponsors:
				for member in unchecked_member_sponsors:
					event.member_sponsor.remove(member)
			if checked_member_sponsors:
				for member in checked_member_sponsors:
					event.member_sponsor.add(Member.objects.get(pk=member))

			if unchecked_member_volunteers:
				for member in unchecked_member_volunteers:
					event.member_volunteer.remove(member)
			if checked_member_volunteers:
				for member in checked_member_volunteers:
					event.member_volunteer.add(Member.objects.get(pk=member))

			if 'Draft' in request.POST: event.status = 'Draft'
			event.save()

			UserLog.objects.create(user = request.user, description = "Event Updated. (%s)" % (event.title,),)

			if 'Yes' in request.POST:
				t = threading.Thread(target=send_event_updated_notification(event))
				t.setDaemon = True
				t.start()

			return redirect('event:event-view', event.slug)
	else:
		event_form = EventForm(instance=event)
		error_message = None

	if event.speakers.all():
		excluded_speakers = [ (speaker.id) for speaker in event.speakers.all() ]
		speaker_list = Speaker.objects.exclude(id__in=excluded_speakers)
		speaker_list_2 = Speaker.objects.filter(id__in=excluded_speakers)
	else:
		speaker_list = Speaker.objects.all()
		speaker_list_2 = None
		
	if event.sponsors.all():
		excluded_sponsors = [ (sponsor.id) for sponsor in event.sponsors.all() ]
		sponsor_list = Sponsor.objects.exclude(id__in=excluded_sponsors)
		sponsor_list_2 = Sponsor.objects.filter(id__in=excluded_sponsors)
	else:
		sponsor_list = Sponsor.objects.all()
		sponsor_list_2 = None

	if event.volunteers.all():
		excluded_volunteers = [ (volunteer.id) for volunteer in event.volunteers.all() ]
		volunteer_list = Volunteer.objects.exclude(id__in=excluded_volunteers)
		volunteer_list_2 = Volunteer.objects.filter(id__in=excluded_volunteers)
	else:
		volunteer_list = Volunteer.objects.all()
		volunteer_list_2 = None

	if event.member_sponsor.all():
		exluded_member_sponsor = [ (member.id) for member in event.member_sponsor.all() ]
		member_sponsor_list = Member.objects.exclude(id__in=exluded_member_sponsor)
		member_sponsor_list_2 = Member.objects.filter(id__in=exluded_member_sponsor)
	else:
		member_sponsor_list =  Member.objects.all()
		member_sponsor_list_2 = None

	if event.member_speaker.all():
		exluded_member_speaker = [ (member.id) for member in event.member_speaker.all() ]
		member_speaker_list = Member.objects.exclude(id__in=exluded_member_speaker)
		member_speaker_list_2 = Member.objects.filter(id__in=exluded_member_speaker)
	else:
		member_speaker_list =  Member.objects.all()
		member_speaker_list_2 = None

	if event.member_volunteer.all():
		excluded_member_volunteer = [ (member.id) for member in event.member_volunteer.all() ]
		member_volunteer_list = Member.objects.exclude(id__in=excluded_member_volunteer)
		member_volunteer_list_2 = Member.objects.filter(id__in=excluded_member_volunteer)
	else:
		member_volunteer_list =  Member.objects.all()
		member_volunteer_list_2 = None

	speaker_form = SpeakerForm()
	sponsor_form = SponsorForm()
	volunteer_form = VolunteerForm()

	context = {
		'event': event,
		'event_form': event_form, 'speaker_form': speaker_form, 'sponsor_form': sponsor_form, 'volunteer_form': volunteer_form,
		'speaker_list': speaker_list, 'speaker_list_2': speaker_list_2, 'sponsor_list': sponsor_list, 
		'sponsor_list_2': sponsor_list_2, 'volunteer_list': volunteer_list, 'volunteer_list_2': volunteer_list_2,
		'member_speaker_list': member_speaker_list, 'member_speaker_list_2': member_speaker_list_2, 'member_sponsor_list': member_sponsor_list,
		'member_sponsor_list_2': member_sponsor_list_2, 'member_volunteer_list': member_volunteer_list, 'member_volunteer_list_2': member_volunteer_list_2,
		'error_message': error_message,}
	return render(request, 'event/event-update.html', context)


@login_required
def delete_event(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	event = get_object_or_404(Event, slug=slug)
	UserLog.objects.create(user = request.user, description = "Event Removed. (%s)" % (event.title,),)
	event.delete()
	return redirect('event:event-upcoming')


@login_required
def publish_event(request, slug, notif):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	date_now = datetime.datetime.now().date()
	event = get_object_or_404(Event, slug=slug)
	event.status = 'Publish'
	event.save()
	if notif == 1:
		send_event_notification(event)
	UserLog.objects.create(user = request.user, description = "Event Published. (%s)" % (event.title,),)
	if date_now >= event.date:
		return redirect('event:event-past')
	else:
		return redirect('event:event-upcoming')


@login_required
def list_draft(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	event_list = Event.objects.exclude(status='Publish')
	context = {'event_list': event_list,}
	return render(request, 'event/event-draft.html', context)


@login_required
def list_published(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	event_list = Event.objects.filter(author=request.user, status='Publish').order_by('-date_to')
	context = {'event_list': event_list}
	return render(request, 'event/event-published.html', context)


def create_feedback(request, slug):
	event = get_object_or_404(Event, slug=slug)
	if request.method == 'POST':
		feedback_form = FeedbackForm(request.POST)
		if feedback_form.is_valid():
			feedback = feedback_form.save(commit=False)
			feedback.event = event
			feedback.save()
			if request.user.is_anonymous:
				UserLog.objects.create(description = "New Event Feedback. (%s)" % (event.title,),)
			else:
				UserLog.objects.create(user = request.user,description = "New Event Feedback. (%s)" % (event.title,),)

			feedback_notif_thread = threading.Thread(target=send_feedback_notification(feedback))
			feedback_notif_thread.setDaemon = True
			feedback_notif_thread.start()

			return redirect('event:event-feedback', event.slug)
	else:
		feedback_form = FeedbackForm()
	context = {'feedback_form': feedback_form,'event': event,}
	return render(request, 'event/event-feedback-create.html', context)


def list_feedback(request, slug):
	event = get_object_or_404(Event, slug=slug)
	feedback_list = Feedback.objects.filter(event=event).order_by('-timestamp')
	context = {'feedback_list': feedback_list,'event': event,}
	return render(request, 'event/event-feedback.html', context)


@login_required
def delete_feedback(request, slug, pk):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	event = Event.objects.get(slug=slug)
	feedback = get_object_or_404(Feedback, event = event, pk = pk)
	UserLog.objects.create(user = request.user,description = "Event Feedback Removed. (%s)" % (event.title,),)
	feedback.delete()
	return redirect('event:event-feedback', slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def event_data(request):
	date_now = datetime.datetime.now().date()
	date_from = request.GET.get('from')
	date_to = request.GET.get('to')
	title = request.GET.get('title') if request.GET.get('title') else ''
	status = request.GET.getlist('status')


	if 'past' in status and 'upcoming' in status:
		event_list = Event.objects.filter((Q(date__range=(date_from, date_to)) & Q(title__contains=title))).order_by('-date')
	elif 'past' in status:
		event_list = Event.objects.filter((Q(date_to__range=(date_from, date_to)) & Q(title__contains=title)) & Q(date_to__lte=date_now)).order_by('-date_to')
	elif 'upcoming' in status:
		event_list = Event.objects.filter((Q(date__range=(date_from, date_to)) & Q(title__contains=title)) & Q(date__gte=date_now)).order_by('-date')
	else:
		event_list = Event.objects.filter((Q(date__range=(date_from, date_to)) & Q(title__contains=title))).order_by('-date')

	top_attendee = EventAttendance.objects.values('member_name').annotate(num_events=Count('member_id')).order_by('-num_events', 'member_name')[:8]
	gender_count = EventStatistics.objects.aggregate(Sum('manual_count'), Sum('male'), Sum('female'))

	if not (gender_count['manual_count__sum'] == None or gender_count['manual_count__sum'] == 0):
		gender_percentage = {
			'male': round((int(gender_count['male__sum'])/int(gender_count['manual_count__sum']))*100, 2),
			'female': round((int(gender_count['female__sum'])/int(gender_count['manual_count__sum']))*100, 2),}
	else:
		gender_percentage = {'male': 0, 'female': 0,}
		gender_count['male__sum'], gender_count['female__sum'], gender_count['manual_count__sum'] = 0, 0, 0

	context = {'gender_count': gender_count, 'gender_percentage': gender_percentage, 'top_attendee':top_attendee,'event_list': event_list,}
	return render(request, 'event/event-data.html', context)


@user_passes_test(lambda u: u.is_superuser)
def event_data_sync(request, slug):
	event = Event.objects.get(slug=slug)
	meetup_event_attendance = settings.MEETUP_CLIENT.GetGroupEventsAttendance({'id': event.meetup_ID, 'urlname': 'gdgzamboanga'})
	meetup_event_rsvps = settings.MEETUP_CLIENT.GetRsvps({'event_id': event.meetup_ID})

	if EventStatistics.objects.filter(event=event).exists():
		event_statistic = get_object_or_404(EventStatistics, event=event)
		event_statistic.yes_rsvp = meetup_event_rsvps.results[0]['tallies']['yes']
		event_statistic.no_rsvp = meetup_event_rsvps.results[0]['tallies']['no']
		event_statistic.manual_count = meetup_event_rsvps.results[0]['tallies']['yes']
		event_statistic.save()
	else:
		event_statistic = get_object_or_404(EventStatistics, event=event)
		event_statistic.yes_rsvp = meetup_event_rsvps.results[0]['tallies']['yes']
		event_statistic.no_rsvp = meetup_event_rsvps.results[0]['tallies']['no']
		event_statistic.save()
	
	if EventAttendance.objects.filter(event_statistic=event_statistic).exists():
		existing_attendace = EventAttendance.objects.filter(event_statistic=event_statistic)
		member_id_list = [ member.member_id for member in existing_attendace ]

		for member in meetup_event_attendance.items:
			if not str(member['member']['id']) in member_id_list:
				EventAttendance.objects.create(
					event_statistic = event_statistic,
					member_id = member['member']['id'],
					member_name = member['member']['name'],
				)
	else:
		for member in meetup_event_attendance.items:
			EventAttendance.objects.create(
				event_statistic = event_statistic,
				member_id = member['member']['id'],
				member_name = member['member']['name'],
			)
	return redirect('event:event-data-details', slug=slug) 


@user_passes_test(lambda u: u.is_superuser)
def event_data_details(request, slug):
	event = Event.objects.get(slug=slug)
	event_statistic = get_object_or_404(EventStatistics, event=event)
	event_attendance = EventAttendance.objects.filter(event_statistic=event_statistic)
	if int(event_statistic.manual_count) == 0:
		gender_percentage = {'male': 0, 'female': 0, 'manual_count': 0}
	else:
		gender_percentage = {
			'male': round((int(event_statistic.male)/int(event_statistic.manual_count))*100, 2),
			'female': round((int(event_statistic.female)/int(event_statistic.manual_count))*100, 2),}
	context = { 'event': event, 'event_statistic': event_statistic, 'event_attendance': event_attendance, 'gender_percentage': gender_percentage,}
	return render(request, 'event/event-data-details.html', context)


@user_passes_test(lambda u: u.is_superuser)
def attendees_list(request):
	attendee_list = EventAttendance.objects.values('member_name').annotate(num_events=Count('member_id')).order_by('-num_events', 'member_name')
	context = {'attendee_list': attendee_list,}
	return render(request, 'event/event-data-attendees.html', context)


@user_passes_test(lambda u: u.is_superuser)
def event_gender_count_update(request, slug):
	event = Event.objects.get(slug=slug)
	event_statistic = get_object_or_404(EventStatistics, event=event)
	error_message = None
	if request.method == 'POST':
		form = EventStatisticForm(request.POST, instance=event_statistic)
		if form.is_valid():
			statistic = form.save(commit=False)
			if int(event_statistic.manual_count) == (int(statistic.male) + int(statistic.female)):
				statistic.save()
				return redirect('event:event-data-details', slug=slug)
			else:
				error_message = "Ooops! Total number of Males and Females does'nt match with the total RSVP/Manual Count."
	else:
		form = EventStatisticForm(instance=event_statistic)
	context = {'error_message': error_message, 'event_statistic': event_statistic,'form': form,}
	return render(request, 'event/event-data-gender-count.html', context)


@user_passes_test(lambda u: u.is_superuser)
def event_manual_count_update(request, slug):
	event = Event.objects.get(slug=slug)
	event_statistic = get_object_or_404(EventStatistics, event=event)
	error_message = None
	if request.method == 'POST':
		form = EventStatisticManualCountForm(request.POST, instance=event_statistic)
		if form.is_valid():
			statistic = form.save(commit=False)
			if int(event_statistic.yes_rsvp) <= int(statistic.manual_count):
				statistic.save()
				return redirect('event:event-data-details', slug=slug)
			else:
				error_message = "Ooops! Manual count is less than RSVP."
	else:
		form = EventStatisticManualCountForm(instance=event_statistic)
	context = {'error_message': error_message, 'event_statistic': event_statistic, 'form': form,}
	return render(request, 'event/event-data-manual-count.html', context)


@user_passes_test(lambda u: u.is_superuser)
def event_statistic_pdf(request, slug):
	event = Event.objects.get(slug=slug)
	event_statistic = EventStatistics.objects.get(event=event)
	event_attendance = EventAttendance.objects.filter(event_statistic=event_statistic)
	context = {
		'event_statistic': event_statistic,
		'event_attendance': event_attendance,
	}
	pdf = render_to_pdf('event/event-pdf.html', context)
	return HttpResponse(pdf, content_type='application/pdf')