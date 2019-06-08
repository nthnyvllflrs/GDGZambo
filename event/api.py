import datetime
import requests

from bs4 import BeautifulSoup

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Speaker, Sponsor , Event, EventStatistics, EventAttendance

@api_view(['POST'])
def create_speaker_api(request):
	firstname = request.POST.get('firstname', None)
	lastname = request.POST.get('lastname', None)
	email = request.POST.get('email', None)
	description = request.POST.get('description', None)
	expertise = request.POST.get('expertise', None)
	facebook = request.POST.get('facebook', None)
	twitter = request.POST.get('twitter', None)
	instagram = request.POST.get('instagram', None)
	website = request.POST.get('website', None)

	facebook_valid = True
	if facebook != '':
		request = requests.get('https://www.facebook.com/' + facebook)
		facebook_valid = True if request.status_code == 200 else False

	twitter_valid = True
	if twitter != '':
		request = requests.get('https://www.twitter.com/' + twitter)
		twitter_valid = True if request.status_code == 200 else False

	instagram_valid = True
	if instagram != '':
		request = requests.get('https://www.instagram.com/' + instagram)
		instagram_valid = True if request.status_code == 200 else False

	if facebook_valid and twitter_valid and instagram_valid:
		speaker = Speaker.objects.create(
			name = firstname + ' ' + lastname, firstname = firstname, lastname = lastname, email = email, description = description, 
			expertise = expertise, facebook = facebook, twitter = twitter, instagram = instagram, website = website,)
		data = { 'id': speaker.id, 'name': speaker.name, 'description': speaker.description[:50], 'created': True,}
	else:
		data = {'error': 'One of the Social Media URL is invalid. Please supply a valid URL or leave it blank.'}

	return Response(data)


@api_view(['POST'])
def create_sponsor_api(request):
	name = request.POST.get('name', None)
	email = request.POST.get('email', None)
	description = request.POST.get('description', None)
	facebook = request.POST.get('facebook', None)
	twitter = request.POST.get('twitter', None)
	instagram = request.POST.get('instagram', None)
	website = request.POST.get('website', None)

	facebook_valid = True
	if facebook != '':
		request = requests.get('https://www.facebook.com/' + facebook)
		facebook_valid = True if request.status_code == 200 else False

	twitter_valid = True
	if twitter != '':
		request = requests.get('https://www.twitter.com/' + twitter)
		twitter_valid = True if request.status_code == 200 else False

	instagram_valid = True
	if instagram != '':
		request = requests.get('https://www.instagram.com/' + instagram)
		instagram_valid = True if request.status_code == 200 else False

	if facebook_valid and twitter_valid and instagram_valid:
		sponsor = Sponsor.objects.create(
			name = name, email = email, description = description, facebook = facebook, 
			twitter = twitter, instagram = instagram, website = website,)
		data = { 'id': sponsor.id, 'name': sponsor.name, 'description': sponsor.description[:50], 'created': True,}
	else:
		data = {'error': 'One of the Social Media URL is invalid. Please supply a valid URL or leave it blank.'}

	return Response(data)


@api_view(['GET'])
def sync_event_api(request, slug):
	event = Event.objects.get(slug=slug)
	meetup_event = settings.MEETUP_CLIENT.GetEvent({'id': event.meetup_ID})
	meetup_event_attendance = settings.MEETUP_CLIENT.GetGroupEventsAttendance({'id': event.meetup_ID, 'urlname': 'gdgzamboanga'})
	meetup_event_rsvps = settings.MEETUP_CLIENT.GetRsvps({'event_id': event.meetup_ID})

	event_statistic = get_object_or_404(EventStatistics, event=event)
	event_statistic.yes_rsvp = meetup_event_rsvps.results[0]['tallies']['yes']
	event_statistic.no_rsvp = meetup_event_rsvps.results[0]['tallies']['no']
	event_statistic.manual_count = meetup_event.headcount
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

	data = {'success': True,}
	return Response(data)


@api_view(['GET'])
def event_resync(request, slug):
	# Get Event
	event = Event.objects.get(slug=slug)
	# Use Meetup API
	meetup_event = settings.MEETUP_CLIENT.GetEvent({'id': event.meetup_ID})
	# Get Event Title/Name
	event_title = meetup_event.name
	# Get Event Description
	event_description = meetup_event.description if 'description' in  meetup_event.__dict__ else 'No Description'
	event_description = BeautifulSoup(event_description, features='html.parser').get_text(separator='\n')
	# Get Event Banner
	event_banner = meetup_event.photo_url if 'photo_url' in meetup_event.__dict__ else None
	# Get Event Duration
	event_duration = meetup_event.duration if 'duration' in  meetup_event.__dict__ else 0
	# Get Event Start and End Date and Time
	event_start = datetime.datetime.fromtimestamp(meetup_event.time/1000.0)
	event_start_date = event_start.strftime("%Y-%m-%d")
	event_start_time = event_start.strftime("%H:%M:%S")
	event_end = datetime.datetime.fromtimestamp(meetup_event.time/1000.0) + datetime.timedelta(hours=event_duration/3600000)
	event_end_date = event_end.strftime("%Y-%m-%d")
	event_end_time = event_end.strftime("%H:%M:%S")
	# Get Event Location
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

	data = {
		'name': event_title, 'description': event_description, 'banner': event_banner,
		'start_date': event_start_date, 'start_time': event_start_time, 'end_date': event_end_date, 'end_time': event_end_time,
		'location': event_location, 'latitude': event_lat, 'longitude': event_lng,}
	return Response(data)