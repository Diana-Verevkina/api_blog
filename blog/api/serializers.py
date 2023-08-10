import datetime as dt
from django.contrib.auth import get_user_model
from news.models import Blog, Post, Follow
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

#User = get_user_model()



class PostsSerializer(serializers.ModelSerializer):
    """Сериализер для модели Post."""
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'header', 'text', 'pub_date', 'author', 'blog')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'blog'])]

    def validate_blog(self, data):
        myblog = Blog.objects.get(user=self.context['request'].user)
        if myblog != data:
            return data
        raise serializers.ValidationError('Нельзя подписаться на свой блог')
