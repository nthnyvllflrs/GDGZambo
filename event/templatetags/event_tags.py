from datetime import datetime, date, timedelta
from django import template
from event.models import Speaker
from team.models import Member

register = template.Library()

@register.simple_tag
def check_conflict_speaker(speaker, start_date, end_date, event=''):
	start_date, end_date = datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d")
	event_days = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((end_date-start_date).days + 1)]

	speaker = Speaker.objects.get(name=speaker)
	event_set = speaker.event_set.all()
	event_set = event_set.exclude(title=event)
	speaker_days = []
	for event in event_set:
		days = [(event.date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((event.date_to-event.date).days + 1)]
		speaker_days += days

	for day in event_days:
		if day in speaker_days:
			return True
	return False

@register.simple_tag
def check_conflict_member(member, start_date, end_date, event=''):
	start_date, end_date = datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d")
	event_days = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((end_date-start_date).days + 1)]

	member = Member.objects.get(name=member)
	event_set = member.event_set.all()
	event_set = event_set.exclude(title=event)
	member_days = []
	for event in event_set:
		days = [(event.date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((event.date_to-event.date).days + 1)]
		member_days += days

	for day in event_days:
		if day in member_days:
			return True
	return False