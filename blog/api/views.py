from django.shortcuts import render
from rest_framework import viewsets, mixins
from news.models import Blog, Post, Follow, User
from .serializers import PostsSerializer, FollowSerializer
from rest_framework.pagination import PageNumberPagination, \
    LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .mixins import LikedMixin


class PostsViewSet(viewsets.ModelViewSet, LikedMixin):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    #pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
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


class NewsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, LikedMixin):
    serializer_class = PostsSerializer
    #pagination_class = PageNumberPagination
    pagination_class = LimitOffsetPagination
    ordering_fields = ['pub_date']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        #followed_people = User.objects.filter(follower__user=self.request.user).all()
        #followed_people = Follow.objects.filter(user=self.request.user).all()
        #authors = self.request.user.follower.all()
        #posts = Post.objects.filter(author__follower__user=self.request.user)
        #posts = Post.objects.filter(author__follower__user=self.request.user)
        #blog = Blog.objects.get(user=self.request.user)
        #return Post.objects.filter(author__in=followed_people.following).all()
        # return Post.objects.filter(author__follower=self.request.user)
        # return posts
        followed_people = Follow.objects.filter(user=self.request.user).values_list('blog_author', flat=True)
        print('--------------------------------------')
        print(followed_people)
        return Post.objects.filter(author__in=followed_people).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
