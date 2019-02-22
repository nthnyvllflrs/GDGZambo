from django.urls import path

from .views import (
	list_blog,
	list_draft_blog,
	list_published_blog,
	list_waiting_blog,

	view_blog,
	create_blog,
	update_blog,
	delete_blog,
	publish_blog,

	add_view_photos,
	delete_photo,

	list_comment,
	create_comment,
	delete_comment,
)

urlpatterns = [
	path('', list_blog, name='blog-list'),
	path('draft/', list_draft_blog, name='blog-draft'),
	path('published/', list_published_blog, name='blog-published'),
	path('waiting/', list_waiting_blog, name='blog-waiting'),

	path('create/', create_blog, name='blog-create'),
	path('<slug:slug>/', view_blog, name='blog-view'),
	path('<slug:slug>/update/', update_blog, name='blog-update'),
	path('<slug:slug>/delete/', delete_blog, name='blog-delete'),
	path('<slug:slug>/publish/<int:notif>', publish_blog, name='blog-publish'),

	path('<slug:slug>/photos/', add_view_photos, name='blog-photo'),
	path('<slug:slug>/photo/<int:pk>/', delete_photo, name='blog-photo-delete'),

	path('<slug:slug>/comment/', list_comment, name='blog-comment'),
	path('<slug:slug>/comment/create/', create_comment, name='blog-comment-create'),
	path('<slug:slug>/comment/<int:pk>/delete/', delete_comment, name='blog-comment-delete'),
]