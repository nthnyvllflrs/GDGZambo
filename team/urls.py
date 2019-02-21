from django.urls import path

from .views import (
	list_member_volunteer,

	create_member,
	update_member,
	delete_member,

	create_volunteer,
	update_volunteer,
	delete_volunteer,
	migrate_volunteer,
)

urlpatterns = [
	path('', list_member_volunteer, name='list-member-volunteer'),

	path('create/', create_member, name='create-member'),
	path('<slug:slug>/update/', update_member, name='update-member'),
	path('<slug:slug>/delete/', delete_member, name='delete-member'),

	path('volunteer/create/', create_volunteer, name='create-volunteer'),
	path('volunteer/<slug:slug>/update/', update_volunteer, name='update-volunteer'),
	path('volunteer/<slug:slug>/delete/', delete_volunteer, name='delete-volunteer'),
	path('volunteer/<slug:slug>/migrate/', migrate_volunteer, name='migrate-volunteer'),
]