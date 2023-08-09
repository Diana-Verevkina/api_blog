import datetime as dt
from django.contrib.auth import get_user_model
from news.models import Post
from rest_framework import serializers

#User = get_user_model()


class PostsSerializer(serializers.ModelSerializer):
    """Сериализер для модели Post."""
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)

    class Meta:
        model = Post
        fields = ('id', 'header', 'text', 'pub_date', 'author')
