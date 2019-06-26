from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import Member, Volunteer
from .forms import MemberForm, VolunteerForm

from user.models import UserLog, UserAccount


def list_member_volunteer(request):
	member_list = Member.objects.all()
	volunteer_list = Volunteer.objects.all()
	context = {'member_list': member_list, 'volunteer_list': volunteer_list,}
	return render(request, 'team/list-member-volunteer.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_member(request):
	member, success = None, False
	if request.method == 'POST':
		member_form = MemberForm(request.POST, request.FILES)
		if member_form.is_valid():
			member = member_form.save(commit=False)
			member.name = member_form.cleaned_data['firstname'] + ' ' + member_form.cleaned_data['lastname']
			member.save()
			UserLog.objects.create(user = request.user, description = "New Member Created. (%s)" % (member.name,),)
			return redirect('team:list-member-volunteer')
	else:
		member_form = MemberForm()
	context = {'member': member, 'member_form': member_form, 'success': success,}
	return render(request, 'team/create-member.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_member(request, slug):
	member = get_object_or_404(Member, slug=slug)
	if request.method == 'POST':
		member_form = MemberForm(request.POST, request.FILES, instance=member)
		if member_form.is_valid():
			member = member_form.save(commit=False)
			member.name = member_form.cleaned_data['firstname'] + ' ' + member_form.cleaned_data['lastname']
			member.save()
			UserLog.objects.create(user = request.user, description = "Member Updated. (%s)" % (member.name,),)
			return redirect('team:list-member-volunteer')
	else:
		member_form = MemberForm(instance=member)
	context = {'member': member, 'member_form': member_form}
	return render(request, 'team/update-member.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_member(request, slug):
	member = get_object_or_404(Member, slug=slug)
	if UserAccount.objects.filter(member=member).exists():
		useraccount = get_object_or_404(UserAccount, member=member)
		user = get_object_or_404(User, username=useraccount.user.username)
		user.delete()
		useraccount.delete()
	UserLog.objects.create(user = request.user, description = "Member Removed. (%s)" % (member.name,),)
	member.delete()
	return redirect('team:list-member-volunteer')


@login_required
def create_volunteer(request):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	volunteer, success = None, False
	if request.method == 'POST':
		volunteer_form = VolunteerForm(request.POST, request.FILES)
		if volunteer_form.is_valid():
			volunteer = volunteer_form.save(commit=False)
			volunteer.name = volunteer_form.cleaned_data['firstname'] + ' ' + volunteer_form.cleaned_data['lastname']
			volunteer.save()
			UserLog.objects.create(user = request.user, description = "New Volunteer Created. (%s)" % (volunteer.name,),)
			return redirect('team:list-member-volunteer')
	else:
		volunteer_form = VolunteerForm()
	context = {'volunteer': volunteer, 'volunteer_form': volunteer_form, 'success': success,}
	return render(request, 'team/create-volunteer.html', context)


@login_required
def update_volunteer(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	volunteer = get_object_or_404(Volunteer, slug=slug)
	if request.method == 'POST':
		volunteer_form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
		if volunteer_form.is_valid():
			volunteer = volunteer_form.save(commit=False)
			volunteer.name = volunteer_form.cleaned_data['firstname'] + ' ' + volunteer_form.cleaned_data['lastname']
			volunteer.save()
			UserLog.objects.create(user = request.user, description = "Volunteer Updated. (%s)" % (volunteer.name,),)
			return redirect('team:list-member-volunteer')
	else:
		volunteer_form = VolunteerForm(instance=volunteer)
	context = {'volunteer': volunteer, 'volunteer_form': volunteer_form}
	return render(request, 'team/update-volunteer.html', context)


@login_required
def delete_volunteer(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_event_creator:
		return redirect('landing-page')
	volunteer = get_object_or_404(Volunteer, slug=slug)
	UserLog.objects.create(user = request.user, description = "Volunteer Removed. (%s)" % (volunteer.name,),)
	volunteer.delete()
	return redirect('team:list-member-volunteer')


@user_passes_test(lambda u: u.is_superuser)
def migrate_volunteer(request, slug):
	volunteer = get_object_or_404(Volunteer, slug=slug)
	volunteered_events = volunteer.event_set.all()
	member = Member.objects.create(
		photo = volunteer.photo, name = volunteer.name, firstname = volunteer.firstname, lastname = volunteer.lastname,
		email = volunteer.email, description = volunteer.description, expertise = volunteer.expertise, facebook = volunteer.facebook,
		twitter = volunteer.twitter, instagram = volunteer.instagram, website = volunteer.website, position = 'Volunteer')
	for event in volunteered_events:
		event.member_volunteer.add(member)
	volunteer.delete()
	return redirect('team:list-member-volunteer')