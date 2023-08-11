from news import services as read_services
from news.models import Blog, Post, Follow
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class PostsSerializer(serializers.ModelSerializer):
    """Сериализер для модели Post."""
    is_read = serializers.SerializerMethodField()
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'header', 'text', 'pub_date', 'author', 'blog',
                  'total_reads', 'is_read')

    def get_is_read(self, obj) -> bool:
        """Проверяет, прочитал ли `request.user` пост (`obj`).
        """
        user = self.context.get('request').user
        return read_services.is_read(obj, user)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              fields=['user', 'blog'])]

    def validate_blog(self, data):
        myblog = Blog.objects.get(user=self.context['request'].user)
        if myblog != data:
            return data
        raise serializers.ValidationError('Нельзя подписаться на свой блог')
