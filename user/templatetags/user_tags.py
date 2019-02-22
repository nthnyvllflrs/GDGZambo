from django import template
from user.models import DynamicData

register = template.Library()

@register.simple_tag
def become_a_sponsor_url():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].become_a_sponsor_url

@register.simple_tag
def become_a_volunteer_url():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].become_a_volunteer_url

@register.simple_tag
def speaker_request_url():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].speaker_request_url

@register.simple_tag
def media_kit_url():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].media_kit_url

@register.simple_tag
def photo_gallery_url():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].photo_gallery_url

@register.simple_tag
def google_plus_link():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].google_plus_link

@register.simple_tag
def facebook_link():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].facebook_link

@register.simple_tag
def twitter_link():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].twitter_link

@register.simple_tag
def youtube_link():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].youtube_link

@register.simple_tag
def instagram_link():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].instagram_link

@register.simple_tag
def meetup_link():
    dynamic = DynamicData.objects.filter(pk=1)
    if not dynamic:
        return '#'
    else:
        return dynamic[0].meetup_link
