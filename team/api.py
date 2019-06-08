import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Volunteer

@api_view(['POST'])
def create_volunteer_api(request):
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
		volunteer = Volunteer.objects.create(
			name = firstname + ' ' + lastname, firstname = firstname, lastname = lastname, email = email, description = description, 
			expertise = expertise, facebook = facebook, twitter = twitter, instagram = instagram, website = website,)
		data = {'id': volunteer.id, 'name': volunteer.name, 'description': volunteer.description[:50], 'created': True,}
	else:
		data = {'error': 'One of the Social Media URL is invalid. Please supply a valid URL or leave it blank.'}

	return Response(data)