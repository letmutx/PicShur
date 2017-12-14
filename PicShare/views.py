import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden


from models import PicShurUser, Picture, Friendship
from forms import SignupForm, PhotoUploadForm


@login_required
def add_picture(request):
    if request.method == 'GET':
        return render(request, 'PicShare/uploadform.html', {'form': PhotoUploadForm, 'user': request.user})

    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            owner = request.user
            pic = Picture(owner=owner, caption=form.data['caption'],
                          description=form.data['description'], image=request.FILES['image'])
            pic.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'PicShare/uploadform.html', {'form': form, 'user': request.user})


def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html', {'form': SignupForm})

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password = make_password(form.data['password'])
            profile_pic = request.FILES.get('profile_pic', None) or './default.jpg'
            user = PicShurUser(username=form.data['username'], password=password,
                               email=form.data['email'], first_name=form.data['first_name'],
                               last_name=form.data['last_name'], profile_pic=profile_pic)

            try:
                user.save()
            except IntegrityError as ie:
                return render(request, 'registration/signup.html', {'form': form})

            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'registration/signup.html', {'form': form})



@login_required
def profile(request):
    photos = Picture.objects.filter(owner=request.user)

    return render(request, 'PicShare/profile.html',
                  {'photos': photos, 'media_url': settings.MEDIA_URL, 'user': request.user})


@login_required
def feed(request):
    if not hasattr(request.user, 'friends'):
        return render(request, 'PicShare/feed.html', {'photos': None, 'user': request.user})

    friends = set([user.username for user in request.user.friends.all()])
    feed_photos = Picture.objects.filter(owner__username__in=friends).order_by('-date_added')

    return render(request, 'PicShare/feed.html', {'media_url': settings.MEDIA_URL, 'photos': feed_photos, 'user': request.user})


@login_required
def users_list(request):
    current_user = request.user

    users = PicShurUser.objects.exclude(username=current_user.username)

    return render(request, 'PicShare/userlist.html', {'users': users, 'current_user': current_user})


@login_required
def delete_picture(request, pk):
    try:
        picture = Picture.objects.get(id=pk)
    except Picture.DoesNotExist:
        return Http404()

    if picture.owner != request.user:
        return HttpResponseForbidden()

    path = settings.MEDIA_ROOT + picture.image

    if os.path.isfile(path):
        os.remove(path)

    picture.delete()

    return HttpResponseRedirect(reverse('profile'))


@login_required
def add_friend(request, pk):
    current_user = request.user

    try:
        user = PicShurUser.objects.get(id=pk)
    except PicShurUser.DoesNotExist:
        return HttpResponseForbidden()

    relation, created = Friendship.objects.get_or_create(from_user=current_user, to_user=user)

    if created:
        relation.save()

    return HttpResponseRedirect(reverse('all_users'))


@login_required
def delete_friend(request, pk):
    current_user = request.user

    try:
        user = PicShurUser.objects.get(id=pk)
    except PicShurUser.DoesNotExist:
        return HttpResponseForbidden()

    try:
        friendship = Friendship.objects.get(from_user=current_user, to_user=user)
    except Friendship.DoesNotExist:
        return Http404()

    friendship.delete()

    return HttpResponseRedirect(reverse('all_users'))


@login_required
def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))