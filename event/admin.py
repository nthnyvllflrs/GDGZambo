from django.contrib import admin

from .models import (
	Volunteer, Sponsor, Speaker, Event, Feedback, EventStatistics, EventAttendance, Info,
)

admin.site.register(Volunteer)
admin.site.register(Sponsor)
admin.site.register(Speaker)
admin.site.register(Event)
admin.site.register(Feedback)
admin.site.register(EventStatistics)
admin.site.register(EventAttendance)
admin.site.register(Info)