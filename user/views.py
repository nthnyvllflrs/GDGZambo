# Django imports
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

# Inner App imports
from .models import (Subscriber, UserAccount, UserLog, SiteCarousel, DynamicData,)
from .forms import (UserAccountForm, SubscribeForm, DynamicDataForm)

# Outer App Imports
from team.models import Member


def subscribe_user(request):
	success = False
	if request.method == 'POST':
		subcribe_form = SubscribeForm(request.POST)
		if subcribe_form.is_valid():
			subscriber = subcribe_form.save()
			success = True
			UserLog.objects.create(user = request.user, description = "New Subscriber Attained. (%s)" % (subscriber.name,),)
	else:
		subcribe_form = SubscribeForm()
	context = {'subcribe_form': subcribe_form, 'success': success}
	return render(request, 'user/subscribe-user.html', context)


def unsubscribe_user(request):
	success, NoMatch = None, None
	if request.method == 'POST':
		email = request.POST['email']
		if Subscriber.objects.filter(email=email).exists():
			subscriber = Subscriber.objects.get(email=email)
			UserLog.objects.create(user = request.user, description = "A Subscriber Unsubscribed. (%s)" % (subscriber.name,),)
			subscriber.delete()
			success = True
		else:
			NoMatch = True
	context = {'success': success, 'NoMatch': NoMatch,}
	return render(request, 'user/unsubscribe-user.html', context)


@login_required
def change_password_user(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			UserLog.objects.create(user = request.user, description = "Password Changed. (%s)" % (request.user.username,),)
			return redirect("landing_page")
	else:
		form = PasswordChangeForm(request.user)
	context = {'form': form,}
	return render(request, 'user/change-password-user.html', context)


@user_passes_test(lambda u: u.is_superuser)
def list_user(request):
	user_list = User.objects.exclude(username='admin')
	context = {'user_list': user_list,}
	return render(request, 'user/list-user.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_user(request, slug):
	member = get_object_or_404(Member, slug=slug)
	if request.method == 'POST':
		useraccount_form = UserAccountForm(request.POST)
		if useraccount_form.is_valid():
			useraccount = useraccount_form.save()
			UserAccount.objects.create(user=useraccount, member=member, role=useraccount_form.cleaned_data['role'])
			UserLog.objects.create(user = request.user, description = "New User Account Created. (%s)" % (member.name,),)
			return redirect('user:list-user')
	else:
		useraccount_form = UserAccountForm(initial={'username': str(member.name).replace(" ", "")})
	context = {'member': member, 'useraccount_form': useraccount_form,}
	return render(request, 'user/create-user.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
	user = get_object_or_404(User, pk=pk)
	useraccount = get_object_or_404(UserAccount, user=user)
	UserLog.objects.create(user = request.user, description = "User Account Removed. (%s)" % (user.username,),)
	user.delete()
	useraccount.delete()
	return redirect('user:list-user')


@user_passes_test(lambda u: u.is_superuser)
def change_dynamic_data(request):
	key = DynamicData.objects.filter(pk=1)
	if key:
		if request.method == 'POST':
			dynamic_data_form = DynamicDataForm(request.POST, instance=key[0])
			if dynamic_data_form.is_valid():
				dynamic_data_form.save()
				success = True
		else:
			dynamic_data_form = DynamicDataForm(instance=key[0])
			success = False
	else:
		if request.method == 'POST':
			dynamic_data_form = DynamicDataForm(request.POST)
			if dynamic_data_form.is_valid():
				dynamic_data_form.save()
				success = True
		else:
			dynamic_data_form = DynamicDataForm()
			success = False
		
	context = {'dynamic_data_form': dynamic_data_form, 'success': success, 'key': key,}
	return render(request, 'user/dynamic-data.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_view_site_carousel(request):
	image_list = SiteCarousel.objects.all()
	SiteCarouselFormSet = modelformset_factory(SiteCarousel, fields=('image',), extra=3)

	if request.method == 'POST':
		site_carousel_formset = SiteCarouselFormSet(request.POST, request.FILES)
		if site_carousel_formset.is_valid():
			for f in site_carousel_formset:
				try:
					carousel_item = SiteCarousel(image=f.cleaned_data['image'])
					carousel_item.save()
				except Exception as e:
					continue
			UserLog.objects.create(user = request.user,description = "Site Carousel Updated.",)
			return redirect('user:site-carousel')
	else:
		site_carousel_formset = SiteCarouselFormSet(queryset=SiteCarousel.objects.none())
	context = {'image_list': image_list, 'site_carousel_formset': site_carousel_formset,}
	return render(request, 'user/site-carousel.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_site_carousel(request, pk):
	site_carousel = get_object_or_404(SiteCarousel, pk=pk)
	site_carousel.delete()
	UserLog.objects.create(user = request.user,description = "Site Carousel Image Removed.",)
	return redirect('user:site-carousel')