import datetime
from django.shortcuts import render

from event.models import Event, Speaker
from blog.models import Blog
from story.models import Story
from user.models import DynamicData, SiteCarousel

def landing_page(request):
	date_now = datetime.datetime.now().date()
	gt_event = Event.objects.filter(date__gt=date_now)[:1]
	e_event = Event.objects.filter(date=date_now)[:1]

	blog_list = Blog.objects.filter(status='Publish').order_by('-timestamp')[:1]
	story_list = Story.objects.filter(status='Publish').order_by('-timestamp')[:1]

	image_list = SiteCarousel.objects.all()
	dynamic = DynamicData.objects.filter(pk=1)
	if dynamic:
		about_us = dynamic[0].about_us
	else:
		about_us = "Google Developers Group Zamboanga"
	context = {
		'about_us': about_us, 'image_list': image_list, 'gt_event': gt_event, 
		'e_event': e_event, 'blog_list': blog_list, 'story_list': story_list,}
	return render(request, 'landing-page.html', context)