from django.conf.urls import url
from .views import CreatePostViewSet, CreateOrDeleteLikeViewSet, RetrievePostListViewSet

urlpatterns = [
    url(r'^view/posts/$', RetrievePostListViewSet.as_view()),
    url(r'^create/post/$', CreatePostViewSet.as_view()),
    url(r'^like/$', CreateOrDeleteLikeViewSet.as_view()),
]