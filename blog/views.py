import threading

from django import forms
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from .models import (Blog, Photo, Comment,)
from .forms import (BlogForm, PhotoForm, CommentForm,)

from user.models import UserLog, UserAccount
from user.utils import send_blog_notification, send_blog_published_notification, send_comment_notification

def view_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if blog.status != 'Publish' and not request.user.is_authenticated:
        return redirect('landing-page')
    context = {'blog': blog,}
    return render(request, 'blog/blog-view.html', context)


def list_blog(request):
    blog_list = Blog.objects.filter(status='Publish').order_by('-timestamp')
    context = {'blog_list': blog_list,}
    return render(request, 'blog/blog-list.html', context)


def list_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comment_list = Comment.objects.filter(blog=blog).order_by('-timestamp')
    context = {'comment_list': comment_list, 'blog': blog,}
    return render(request, 'blog/blog-comment.html', context)


def create_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.save()
            if request.user.is_anonymous:
                UserLog.objects.create(description = "New Blog Comment. (%s)" % (blog.title,),)
            else:
                UserLog.objects.create(user = request.user, description = "New Blog Comment. (%s)" % (blog.title,),)

            comment_notif_thread = threading.Thread(target=send_comment_notification(comment))
            comment_notif_thread.setDaemon = True
            comment_notif_thread.start()

            return redirect('blog:blog-comment', blog.slug)
    else:
        comment_form = CommentForm()
    context = {'comment_form': comment_form, 'blog': blog,}
    return render(request, 'blog/blog-comment-create.html', context)


@login_required
def delete_comment(request, slug, pk):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    blog = Blog.objects.get(slug=slug)
    comment = get_object_or_404(Comment, blog = blog, pk = pk)
    UserLog.objects.create(user = request.user, description = "Blog Comment Removed. (%s)" % (blog.title,),)
    comment.delete()
    return redirect('blog:comment-list', slug)


@login_required
def publish_blog(request, slug, notif):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    blog = get_object_or_404(Blog, slug=slug)
    user = get_object_or_404(User, username=blog.author.username)
    if request.user.is_superuser:
        blog.status = 'Publish'
        description = "Blog Publish"
        if not user.is_superuser:
            member_notif_thread = threading.Thread(target=send_blog_published_notification(user.useraccount.member, blog))
            member_notif_thread.setDaemon = True
            member_notif_thread.start()
        if notif == 1:
            blog_notif_thread = threading.Thread(target=send_blog_notification(blog))
            blog_notif_thread.setDaemon = True
            blog_notif_thread.start()
    else:
        blog.status = 'Waiting'
        description = "Blog Waiting Status"
    blog.save()
    UserLog.objects.create(user = request.user, description = description + ". (%s)" % (blog.title,),)
    return redirect('blog:blog-list')


@login_required
def list_draft_blog(request):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    blog_list = Blog.objects.filter(author=request.user).exclude(status='Publish').order_by('-timestamp')
    context = {'blog_list': blog_list,}
    return render(request, 'blog/blog-list.html', context) 


@login_required
def list_published_blog(request):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    blog_list = Blog.objects.filter(author=request.user, status='Publish')
    context = {'blog_list': blog_list,}
    return render(request, 'blog/blog-published.html', context)


@user_passes_test(lambda u: u.is_superuser)
def list_waiting_blog(request):
    blog_list = Blog.objects.filter(status='Waiting')
    context = {'blog_list': blog_list,}
    return render(request, 'blog/blog-waiting.html', context)


@login_required
def create_blog(request):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    PhotoFormSet = modelformset_factory(Photo, fields=('image',),
        widgets={'name': forms.ClearableFileInput(attrs={'class': 'form-control'})}, extra=3,)
    if request.method == 'POST':
        blog_status = 'Draft' if ('Draft' in request.POST) else 'Waiting'
        blog_form = BlogForm(request.POST)
        photo_formset = PhotoFormSet(request.POST, request.FILES)
        if blog_form.is_valid() and photo_formset.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.status = blog_status
            blog.save()
            UserLog.objects.create(user = request.user, description = "New Blog Created. (%s)" % (blog.title,),)
            for f in photo_formset:
                try:
                    photo = Photo(blog=blog, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    continue

            if 'Yes' in request.POST:
                blog.status = 'Publish'
                blog.save()
                t = threading.Thread(target=send_blog_notification(blog))
                t.setDaemon = True
                t.start()
            elif 'No' in request.POST:
                blog.status = 'Publish'
                blog.save()

            return redirect('blog:blog-draft')
    else:
        blog_form = BlogForm()
        photo_formset = PhotoFormSet(queryset=Photo.objects.none())
    context = {'blog_form': blog_form, 'photo_formset': photo_formset,}
    return render(request, 'blog/blog-create.html', context)


@login_required
def update_blog(request, slug):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    updated = False
    blog = get_object_or_404(Blog, slug=slug)
    old_blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, instance=blog)
        if blog_form.is_valid():
            updated_blog = blog_form.save(commit=False)
            if 'Draft' in request.POST:
                updated_blog.status = 'Draft'
                updated_blog.save()
                return redirect('blog:blog-draft')
            else:
                if not (old_blog.title == blog_form.cleaned_data['title'] and 
                    old_blog.body == blog_form.cleaned_data['body'] and old_blog.video_url == blog_form.cleaned_data['video_url']):
                    if blog.status != 'Draft':
                        if request.user.is_superuser:
                            updated_blog.save()
                            return redirect('blog:blog-published')
                        else:
                            updated_blog.status = 'Waiting'
                            updated_blog.save()
                            updated = True
                    else:
                        updated_blog.save()
                        return redirect('blog:blog-draft')
                    UserLog.objects.create(user = request.user, description = "Blog Updated. (%s)" % (updated_blog.title,),)
                else:
                    return redirect('blog:blog-published')
    else:
        blog_form = BlogForm(instance=blog)
    context = {'blog_form': blog_form, 'blog': blog, 'updated': updated,}
    return render(request, 'blog/blog-update.html', context)


@login_required
def delete_blog(request, slug):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    blog = get_object_or_404(Blog, slug=slug)
    UserLog.objects.create(user = request.user, description = "Blog Removed. (%s)" % (blog.title,),)
    blog.delete()
    return redirect('blog:blog-list')


@login_required
def add_view_photos(request, slug):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    updated = False
    blog = get_object_or_404(Blog, slug=slug)
    PhotoFormSet = modelformset_factory(Photo, fields=('image',), extra=3)
    if request.method == 'POST':
        photo_formset = PhotoFormSet(request.POST, request.FILES)
        if photo_formset.is_valid():
            for f in photo_formset:
                try:
                    photo = Photo(blog=blog, image=f.cleaned_data['image'])
                    photo.save()
                    updated = True
                except Exception as e:
                    continue
            if updated and not request.user.is_superuser and not blog.status == 'Draft':
                blog.status = 'Waiting'
                blog.save()
            UserLog.objects.create(user = request.user, description = "New Blog Photo Uploaded. (%s)" % (blog.title,),)
            return redirect('blog:blog-photo', slug=blog.slug)
    photo_formset = PhotoFormSet(queryset=Photo.objects.none())
    photo_set = Photo.objects.filter(blog=blog)
    context = {'photo_formset': photo_formset, 'photo_set': photo_set, 'updated': updated, 'blog': blog}
    return render(request, 'blog/blog-photo.html', context)


@login_required
def delete_photo(request, slug, pk):
    if not request.user.is_superuser and not request.user.useraccount.is_blog_creator:
        return redirect('landing-page')
    blog = get_object_or_404(Blog, slug=slug)
    photo = get_object_or_404(Photo, blog=blog, pk=pk)
    UserLog.objects.create(user = request.user, description = "Blog Photo Removed. (%s)" % (blog.title,),)
    photo.delete()
    return redirect('blog:blog-photo', slug=slug)