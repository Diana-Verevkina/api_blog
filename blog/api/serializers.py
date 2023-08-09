import datetime as dt
from django.contrib.auth import get_user_model
from news.models import Post, Follow
from rest_framework import serializers

#User = get_user_model()
from rest_framework.validators import UniqueTogetherValidator


class PostsSerializer(serializers.ModelSerializer):
    """Сериализер для модели Post."""
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)

    class Meta:
        model = Post
        fields = ('id', 'header', 'text', 'pub_date', 'author')
        #required = ('header',)


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'blog'])]

    def validate_author(self, data):
        print(data)
        if self.context['request'].user != data:
            return data
        raise serializers.ValidationError('Нельзя подписаться на себя')