from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Speaker, Sponsor

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