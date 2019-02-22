from django.urls import path

from .views import(
	list_speaker,
	create_speaker,
	update_speaker,
	delete_speaker,

	list_sponsor,
	create_sponsor,
	update_sponsor,
	delete_sponsor,
)

urlpatterns = [
	path('speaker/', list_speaker, name='speaker-list'),
	path('speaker/create/', create_speaker, name='speaker-create'),
	path('speaker/<slug:slug>/update/', update_speaker, name='speaker-update'),
	path('speaker/<slug:slug>/delete/', delete_speaker, name='speaker-delete'),

	path('sponsor/', list_sponsor, name='sponsor-list'),
	path('sponsor/create/', create_sponsor, name='sponsor-create'),
	path('sponsor/<slug:slug>/update/', update_sponsor, name='sponsor-update'),
	path('sponsor/<slug:slug>/delete/', delete_sponsor, name='sponsor-delete'),
]