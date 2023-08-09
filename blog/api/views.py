from django.shortcuts import render
from rest_framework import viewsets
from news.models import Post
from .serializers import PostsSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    #pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    ordering_fields = ['pub_date']
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
