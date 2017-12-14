from __future__ import unicode_literals

from django.contrib.auth.models import UserManager, User
from django.db import models


class PicShurUser(User):
    friends = models.ManyToManyField('self', through='Friendship',
                                     related_name='friends_list', symmetrical=False)

    profile_pic = models.ImageField(default='./default.jpg')

    objects = UserManager()


class Friendship(models.Model):
    from_user = models.ForeignKey(PicShurUser, related_name='from_user')
    to_user = models.ForeignKey(PicShurUser, related_name='to_user')


class Picture(models.Model):
    caption = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    owner = models.ForeignKey(PicShurUser)
    image = models.ImageField(upload_to='')
    date_added = models.DateTimeField(auto_now=True)
