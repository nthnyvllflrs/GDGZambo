from django.urls import path

from .views import(
	list_speaker, create_speaker, update_speaker, delete_speaker,

	list_sponsor, create_sponsor, update_sponsor, delete_sponsor,

	list_upcoming_events, list_past_events, list_published, list_draft,
	view_event, create_pre_event, create_event, update_event, delete_event,
	publish_event,
)

from .api import (
	create_speaker_api, create_sponsor_api,
)

urlpatterns = [
	path('api/speaker/create/', create_speaker_api, name='speaker-create-api'),
	path('api/sponsor/create/', create_sponsor_api, name='sponsor-create-api'),

	path('speaker/', list_speaker, name='speaker-list'),
	path('speaker/create/', create_speaker, name='speaker-create'),
	path('speaker/<slug:slug>/update/', update_speaker, name='speaker-update'),
	path('speaker/<slug:slug>/delete/', delete_speaker, name='speaker-delete'),

	path('sponsor/', list_sponsor, name='sponsor-list'),
	path('sponsor/create/', create_sponsor, name='sponsor-create'),
	path('sponsor/<slug:slug>/update/', update_sponsor, name='sponsor-update'),
	path('sponsor/<slug:slug>/delete/', delete_sponsor, name='sponsor-delete'),

	path('upcoming/', list_upcoming_events, name='event-upcoming'),
	path('past/', list_past_events, name='event-past'),
	path('published/', list_published, name='event-published'),
	path('draft/', list_draft, name='event-draft'),
	path('pre-create/', create_pre_event, name='event-pre-create'),
	path('create/<int:meetup_id>/', create_event, name='event-create'),
	path('<slug:slug>/', view_event, name='event-view'),
	path('<slug:slug>/update/', update_event, name='event-update'),
	path('<slug:slug>/delete/', delete_event, name='event-delete'),
	path('<slug:slug>/publish/<int:notif>/', publish_event, name='event-publish'),
]