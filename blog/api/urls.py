from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import PostsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('posts', PostsViewSet, basename='news')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    ]
