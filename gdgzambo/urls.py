from django.contrib import admin
from django.urls import path, include

from .views import (landing_page,)

urlpatterns = [
    path('', landing_page, name='landing-page'),
    
    path('event/', include(('event.urls', 'event'), namespace='event')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('story/', include(('story.urls', 'story'), namespace='story')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('team/', include(('team.urls', 'team'), namespace='team')),

    path('admin/', admin.site.urls),
]
