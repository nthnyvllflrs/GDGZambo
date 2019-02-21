# Django imports
from django.contrib.auth.models import User
from django.shortcuts import render

# Inner App imports
from .models import (Subscriber, UserAccount, UserLog, SiteCarousel, DynamicData,)

# SuperuserDecorator
def list_user(request):
	user_list = User.objects.exclude(username='admin')
	context = {
		'user_list': user_list,
	}
	return render(request, 'user/user-list.html', context)
