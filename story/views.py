import threading

from django import forms
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from .models import Story, Image
from .forms import StoryForm

from user.models import UserLog
from user.utils import send_story_notification, send_story_published_notification


def view_story(request, slug):
	story = get_object_or_404(Story, slug=slug)
	if story.status != 'Publish' and not request.user.is_authenticated:
		return redirect('landing-page')
	context = {'story': story,}
	return render(request, 'story/story-view.html', context)


def list_story(request):
	story_list = Story.objects.filter(status='Publish').order_by('-timestamp')
	context = {'story_list': story_list,}
	return render(request, 'story/story-list.html', context)


@login_required
def publish_story(request, slug, notif):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	story = get_object_or_404(Story, slug=slug)
	user = get_object_or_404(User, username=story.author.username)
	if request.user.is_superuser:
		story.status = 'Publish'
		description = "Story Publish"
		if not user.is_superuser:
			member_notif_thread = threading.Thread(target=send_story_published_notification(user.useraccount.member, story))
			member_notif_thread.setDaemon = True
			member_notif_thread.start()
		if notif == 1:
			story_notif_thread = threading.Thread(target=send_story_notification(story))
			story_notif_thread.setDaemon = True
			story_notif_thread.start()
	else:
		story.status = 'Waiting'
		description = "Story Waiting Status"
	story.save()
	UserLog.objects.create(user = request.user, description = description + ". (%s)" % (story.title,),)
	return redirect('story:story-list')


@login_required
def list_draft_story(request):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	story_list = Story.objects.filter(author=request.user).exclude(status='Publish').order_by('-timestamp')
	context = {'story_list': story_list,}
	return render(request, 'story/story-list.html', context) 


@login_required
def list_published_story(request):
	story_list = Story.objects.filter(author=request.user, status='Publish')
	context = {'story_list': story_list,}
	return render(request, 'story/story-published.html', context)


@user_passes_test(lambda u: u.is_superuser)
def list_waiting_story(request):
	story_list = Story.objects.filter(status='Waiting')
	context = {'story_list': story_list,}
	return render(request, 'story/story-waiting.html', context)


@login_required
def create_story(request):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	ImageFormSet = modelformset_factory(Image, fields=('photo',),
		widgets={'name': forms.ClearableFileInput(attrs={'class': 'form-control'})}, extra=3,)
	if request.method == 'POST':
		story_status = 'Draft' if ('Draft' in request.POST) else 'Waiting'
		story_form = StoryForm(request.POST)
		image_formset = ImageFormSet(request.POST, request.FILES)
		if story_form.is_valid() and image_formset.is_valid():
			story = story_form.save(commit=False)
			story.author = request.user
			story.status = story_status
			story.save()
			UserLog.objects.create(user = request.user, description = "New Story Created. (%s)" % (story.title,),)
			for f in image_formset:
				try:
					image = Image(story=story, photo=f.cleaned_data['photo'])
					image.save()
				except Exception as e:
					continue

			if 'Yes' in request.POST:
				story.status = 'Publish'
				story.save()
				t = threading.Thread(target=send_story_notification(story))
				t.setDaemon = True
				t.start()
			elif 'No' in request.POST:
				story.status = 'Publish'
				story.save()

			return redirect('story:story-draft')
	else:
		story_form = StoryForm()
		image_formset = ImageFormSet(queryset=Image.objects.none())
	context = {'story_form': story_form, 'image_formset': image_formset,}
	return render(request, 'story/story-create.html', context)


@login_required
def update_story(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	updated = False
	story = get_object_or_404(Story, slug=slug)
	old_story = get_object_or_404(Story, slug=slug)
	if request.method == 'POST':
		story_form = StoryForm(request.POST, instance=story)
		if story_form.is_valid():
			updated_story = story_form.save(commit=False)
			if 'Draft' in request.POST:
				updated_story.status = 'Draft'
				updated_story.save()
				return redirect('story:story-draft')
			else:
				if not (old_story.title == story_form.cleaned_data['title'] and 
					old_story.body == story_form.cleaned_data['body'] and old_story.video_url == story_form.cleaned_data['video_url']):
					if story.status != 'Draft':
						if request.user.is_superuser:
							updated_story.save()
							return redirect('story:story-published')
						else:
							updated_story.status = 'Waiting'
							updated_story.save()
							updated = True
					else:
						updated_story.save()
						return redirect('story:story-draft')
					UserLog.objects.create(user = request.user, description = "Story Updated. (%s)" % (story.title,),)
				else:
					return redirect('story:story-published')
	else:
		story_form = StoryForm(instance=story)
	context = {'story_form': story_form, 'story': story, 'updated': updated,}
	return render(request, 'story/story-update.html', context)


@login_required
def delete_story(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	story = get_object_or_404(Story, slug=slug)
	UserLog.objects.create(user = request.user, description = "Story Removed. (%s)" % (story.title,),)
	story.delete()
	return redirect('story:story-list')


@login_required
def add_view_images(request, slug):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	updated = False
	story = get_object_or_404(Story, slug=slug)
	ImageFormSet = modelformset_factory(Image, fields=('photo',), extra=3)
	if request.method == 'POST':
		image_formset = ImageFormSet(request.POST, request.FILES)
		if image_formset.is_valid():
			for f in image_formset:
				try:
					image = Image(story=story, photo=f.cleaned_data['photo'])
					image.save()
					updated = True
				except Exception as e:
					continue
			if updated and not request.user.is_superuser and not story.status == 'Draft':
				story.status = 'Waiting'
				story.save()
			UserLog.objects.create(user = request.user, description = "New Story Image Uploaded. (%s)" % (story.title,),)
			return redirect('story:story-image', slug=story.slug)
	image_formset = ImageFormSet(queryset=Image.objects.none())
	image_set = Image.objects.filter(story=story)
	context = {'image_formset': image_formset, 'image_set': image_set, 'updated': updated, 'story': story,}
	return render(request, 'story/story-image.html', context)


@login_required
def delete_image(request, slug, pk):
	if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
		return redirect('landing-page')
	story = get_object_or_404(Story, slug=slug)
	image = get_object_or_404(Image, story=story, pk=pk)
	UserLog.objects.create(user = request.user, description = "Story Image Removed. (%s)" % (story.title,),)
	image.delete()
	return redirect('story:story-image', slug=slug)