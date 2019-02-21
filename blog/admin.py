from django.contrib import admin

from .models import (Blog, Photo, Comment,)

admin.site.register(Blog)
admin.site.register(Photo)
admin.site.register(Comment)