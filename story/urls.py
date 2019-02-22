from django.urls import path

from .views import (
	list_story,
	list_draft_story,
	list_published_story,
	list_waiting_story,

	view_story,
	create_story,
	update_story,
	delete_story,
	publish_story,

	add_view_images,
	delete_image,
)

urlpatterns = [
	path('', list_story, name='story-list'),
	path('draft/', list_draft_story, name='story-draft'),
	path('published/', list_published_story, name='story-published'),
	path('waiting/', list_waiting_story, name='story-waiting'),

	path('create/', create_story, name='story-create'),
	path('<slug:slug>/', view_story, name='story-view'),
	path('<slug:slug>/update/', update_story, name='story-update'),
	path('<slug:slug>/delete/', delete_story, name='story-delete'),
	path('<slug:slug>/publish/<int:notif>', publish_story, name='story-publish'),

	path('<slug:slug>/images/', add_view_images, name='story-image'),
	path('<slug:slug>/image/<int:pk>/', delete_image, name='story-image-delete'),
]