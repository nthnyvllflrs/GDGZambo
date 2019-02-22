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

	volunteer = Volunteer.objects.create(
		name = firstname + ' ' + lastname, firstname = firstname, lastname = lastname, email = email, description = description, 
		expertise = expertise, facebook = facebook, twitter = twitter, instagram = instagram, website = website,)
	data = {'id': volunteer.id, 'name': volunteer.name, 'description': volunteer.description[:30], 'created': True,}
	return Response(data)