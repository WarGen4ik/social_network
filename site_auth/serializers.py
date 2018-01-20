from pprint import pprint

from django.contrib.auth import get_user_model
from requests import HTTPError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from site_auth.models import User, Profile
import clearbit
from social_network.settings import hunter


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', )


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        try:
            clearbit_data = clearbit.Enrichment.find(email=validated_data['email'], stream=True)
        except HTTPError:
            clearbit_data = None

        if hunter.email_verifier(validated_data['email'])['result'] == 'undeliverable':
            raise ValidationError('Your email did not passed verification ')

        if clearbit_data is None:
            profile_data = {'first_name': None,
                            'last_name': None}
        else:
            profile_data = {'first_name': clearbit_data['person']['name']['givenName'],
                            'last_name': clearbit_data['person']['name']['familyName']}
        serializer = ProfileSerializer(data=profile_data)

        if serializer.is_valid():
            user = get_user_model().objects.create(email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()

            Profile.objects.create(user=user, **profile_data)
            return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}

