# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from site_auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postuser')
    title = models.CharField('Title', max_length=255)
    text = models.TextField('Text')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return '{}  {}'.format(self.user.email, self.title)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_user')
    created_at = models.DateTimeField(default=now)
