# Django Imports
from django.urls import path

# Inner App Imports
from .views import (
	# USER FUNCTIONS
	list_user,
)

urlpatterns = [
	path('list/', list_user, name='user-list'),
]