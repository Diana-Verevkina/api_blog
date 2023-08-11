from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsViewSet, PostsViewSet, FollowViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('posts', PostsViewSet, basename='news')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register('news', NewsViewSet, basename='news')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    ]
