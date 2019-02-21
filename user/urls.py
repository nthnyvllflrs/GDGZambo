# Django Imports
from django.urls import path

# Inner App Imports
from .views import (
	list_user, create_user, delete_user, change_password_user, list_log,
	subscribe_user, unsubscribe_user,
	change_dynamic_data, update_view_site_carousel, delete_site_carousel,)

urlpatterns = [
	path('', list_user, name='list-user'),
	path('dynamic-data/', change_dynamic_data, name='dynamic-data'),
	path('logs/', list_log, name='user-logs'),

	path('subscribe/', subscribe_user, name='subscribe-user'),
	path('unsubscribe/', unsubscribe_user, name='unsubscribe-user'),

	path('change-password/', change_password_user, name='change-password-user'),
	path('create/<slug:slug>/', create_user, name='create-user'),
	path('delete/<int:pk>/', delete_user, name='delete-user'),

	path('site-carousel/', update_view_site_carousel, name='site-carousel'),
	path('site-carousel/<int:pk>/', delete_site_carousel, name='delete-carousel-image'),
]