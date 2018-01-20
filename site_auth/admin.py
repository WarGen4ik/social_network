# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from site_auth.models import User, UserManager, Profile

admin.site.register(User)
admin.site.register(Profile)