from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from .mixins import ReadMixin
from .permissions import IsAuthorOrReadOnly
from .serializers import PostsSerializer, FollowSerializer
from news.models import Blog, Post, Follow


class PostsViewSet(viewsets.ModelViewSet, ReadMixin):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    ordering_fields = ['pub_date']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        blog=Blog.objects.get(user=self.request.user))


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    search_fields = ('user__username', 'blog__blog_name')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        blog = Blog.objects.get(id=self.request.data['blog'])
        serializer.save(user=self.request.user, blog_author=blog.user)


class NewsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, ReadMixin):
    serializer_class = PostsSerializer
    pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    ordering_fields = ['pub_date']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        followed_people = Follow.objects.filter(
            user=self.request.user).values_list('blog_author', flat=True
                                                )
        return Post.objects.filter(author__in=followed_people).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
