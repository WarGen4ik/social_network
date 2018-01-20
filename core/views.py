# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.models import Post, Like
from core.serializers import PostListSerializer, PostSerializer, LikeSerializer


class CreatePostViewSet(CreateAPIView):
    serializer_class = PostSerializer
    model = Post

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrievePostListViewSet(ListAPIView):
    model = Post
    serializer_class = PostListSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return Post.objects.all()


class CreateOrDeleteLikeViewSet(CreateAPIView):
    serializer_class = LikeSerializer
    model = Like

    def create(self, request, *args, **kwargs):
        try:
            like = get_object_or_404(Like, user=request.user.id, post=request.data['post'])
            like.delete()
            return Response(status=status.HTTP_200_OK)
        except Http404:
            request.data['user'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)