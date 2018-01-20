# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core.models import Post, Like

admin.site.register(Post)
admin.site.register(Like)