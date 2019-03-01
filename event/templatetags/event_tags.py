from django import template
from event.models import Speaker

register = template.Library()

@register.simple_tag
def check_conflict(speaker, start_date, end_date):
	speaker = Speaker.objects.get(name=speaker)
	event_set = speaker.event_set.all()
	result = event_set.filter(date__range=(start_date, end_date)).exists()
	return result