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

	speaker = Speaker.objects.create(
		name = firstname + ' ' + lastname, firstname = firstname, lastname = lastname, email = email, description = description, 
		expertise = expertise, facebook = facebook, twitter = twitter, instagram = instagram, website = website,)
	data = { 'id': speaker.id, 'name': speaker.name, 'description': speaker.description[:30], 'created': True,}
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

	sponsor = Sponsor.objects.create(
		name = name, email = email, description = description, facebook = facebook, twitter = twitter, instagram = instagram, website = website,)
	data = { 'id': sponsor.id, 'name': sponsor.name, 'description': sponsor.description, 'created': True,}
	return Response(data)


@api_view(['GET'])
def sync_event_api(request, id):
	event = Event.objects.get(id=id)
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

	data = {'success': True,}
	return Response(data)