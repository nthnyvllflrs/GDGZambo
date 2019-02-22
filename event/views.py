from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import (Sponsor, Speaker, Event, Feedback, EventStatistics, EventAttendance, Info,)
from .forms import (SponsorForm, SpeakerForm, EventForm, FeedbackForm, EventStatisticForm,)

from user.models import UserLog


def list_speaker(request):
	form = SpeakerForm()
	speaker_list = Speaker.objects.order_by('firstname', 'lastname')
	context = {'form': form,'speaker_list': speaker_list,}
	return render(request, 'event/speaker-list.html', context)


@login_required
def create_speaker(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	if request.method == 'POST':
		speaker_form = SpeakerForm(request.POST, request.FILES)
		if speaker_form.is_valid():
			speaker = speaker_form.save(commit=False)
			speaker.name = speaker_form.cleaned_data['firstname'] + ' ' + speaker_form.cleaned_data['lastname']
			speaker.save()
			UserLog.objects.create(user = request.user, description = "New Speaker Created. (%s)" % (speaker.name,),)
			return redirect('event:speaker-list')
	else:
		speaker_form = SpeakerForm()
	context = {'speaker_form': speaker_form}
	return render(request, 'event/speaker-create.html', context)


@login_required
def update_speaker(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	speaker = get_object_or_404(Speaker, slug=slug)
	if request.method == 'POST':
		speaker_form = SpeakerForm(request.POST, request.FILES, instance=speaker)
		if speaker_form.is_valid():
			speaker = speaker_form.save(commit=False)
			speaker.name = speaker_form.cleaned_data['firstname'] + ' ' + speaker_form.cleaned_data['lastname']
			speaker.save()
			UserLog.objects.create(user = request.user, description = "Speaker Updated. (%s)" % (speaker.name,),)
			return redirect('event:speaker-list')
	else:
		speaker_form = SpeakerForm(instance=speaker)
	context = {'speaker': speaker, 'speaker_form': speaker_form}
	return render(request, 'event/speaker-update.html', context)


@login_required
def delete_speaker(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	speaker = get_object_or_404(Speaker, slug=slug)
	UserLog.objects.create(user = request.user, description = "Speaker Removed. (%s)" % (speaker.name,),)
	speaker.delete()
	return redirect('event:speaker-list')


def list_sponsor(request):
	sponsor_list = Sponsor.objects.order_by('name')
	context = {'sponsor_list': sponsor_list,}
	return render(request, 'event/sponsor-list.html', context)


@login_required
def create_sponsor(request):
	if not request.user.is_superuser:
		return redirect('landing-page')
	if request.method == 'POST':
		sponsor_form = SponsorForm(request.POST, request.FILES)
		if sponsor_form.is_valid():
			sponsor = sponsor_form.save(commit=False)
			sponsor.save()
			UserLog.objects.create(user = request.user, description = "New Sponsor Created. (%s)" % (sponsor.name,),)
			return redirect('event:sponsor-list')
	else:
		sponsor_form = SponsorForm()
	context = {'sponsor_form': sponsor_form}
	return render(request, 'event/sponsor-create.html', context)


@login_required
def update_sponsor(request, slug):
	if not request.user.is_superuser:
		return redirect('landing-page')
	sponsor = get_object_or_404(Sponsor, slug=slug)
	if request.method == 'POST':
		sponsor_form = SponsorForm(request.POST, request.FILES, instance=sponsor)
		if sponsor_form.is_valid():
			sponsor = sponsor_form.save(commit=False)
			sponsor.save()
			UserLog.objects.create(user = request.user, description = "Sponsor Updated. (%s)" % (sponsor.name,),)
			return redirect('event:sponsor-list')
	else:
		sponsor_form = SponsorForm(instance=sponsor)
	context = {'sponsor': sponsor, 'sponsor_form': sponsor_form}
	return render(request, 'event/sponsor-update.html', context)


@login_required
def delete_sponsor(request, slug):
	if not request.user.is_superuser:
		return redirect('landing-page')
	sponsor = get_object_or_404(Sponsor, slug=slug)
	UserLog.objects.create(user = request.user, description = "Sponsor Removed. (%s)" % (sponsor.name,),)
	sponsor.delete()
	return redirect('event:sponsor-list')