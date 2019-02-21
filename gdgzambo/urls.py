from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('event/', include(('event.urls', 'event'), namespace='event')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('story/', include(('story.urls', 'story'), namespace='story')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
]
