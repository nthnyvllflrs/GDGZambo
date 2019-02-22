from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import (landing_page,)

from user.forms import LoginForm

urlpatterns = [
    path('', landing_page, name='landing-page'),
    
    path('login/',auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('event/', include(('event.urls', 'event'), namespace='event')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('story/', include(('story.urls', 'story'), namespace='story')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('team/', include(('team.urls', 'team'), namespace='team')),

    path('admin/', admin.site.urls),
]
