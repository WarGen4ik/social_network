from django.conf.urls import url
from .views import CreateUserViewSet, EmailConfirmView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^auth/$', obtain_jwt_token),
    url(r'^register/$', CreateUserViewSet.as_view()),
    url(r'^email/confirm/(?P<hash>.+)/$', EmailConfirmView.as_view()),
]
