from rest_framework import serializers
from core.models import Post, Like
from site_auth.serializers import UserSerializer


class PostListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'text', 'like_count')

    def get_like_count(self, post):
        return Like.objects.filter(post=post).count()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'text')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post')
