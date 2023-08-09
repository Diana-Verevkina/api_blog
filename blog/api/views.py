from django.shortcuts import render
from rest_framework import viewsets, mixins
from news.models import Post, Follow
from .serializers import PostsSerializer, FollowSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    #pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    ordering_fields = ['pub_date']
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    search_fields = ('user__username', 'author__username')

    def get_queryset(self):
        return Follow.objects.all()
"""
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)"""