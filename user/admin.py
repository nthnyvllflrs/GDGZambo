from django.contrib import admin

from .models import (Subscriber, UserAccount, UserLog, SiteCarousel, DynamicData,)

admin.site.register(Subscriber)
admin.site.register(UserAccount)
admin.site.register(UserLog)
admin.site.register(SiteCarousel)
admin.site.register(DynamicData)