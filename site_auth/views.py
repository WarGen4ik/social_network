# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from site_auth.serializers import UserSerializer


class CreateUserViewSet(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'status': True}, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmView(APIView):

    def get(self, request, *args, **kwargs):
        email_hash = request.user.email_hash
        if email_hash:
            if email_hash == kwargs['hash']:
                request.user.email_hash = 'CONFIRMED'
                request.user.save()
                return Response({'status': 'email confirmed'}, status=status.HTTP_200_OK)
        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
