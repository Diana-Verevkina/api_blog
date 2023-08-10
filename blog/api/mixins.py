from news import services
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

#from .serializers import FanSerializer


class LikedMixin:

    @action(detail=True, methods=['post'], permission_classes=[
            permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Лайкает `obj`."""
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['post'], permission_classes=[
            permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """Удаляет лайк с `obj`."""
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    #@action(detail=True, methods=['post'])
    #def fans(self, request, pk=None):
    #    """Получает всех пользователей, которые лайкнули `obj`."""
    #    obj = self.get_object()
    #    fans = services.get_fans(obj)
    #    serializer = FanSerializer(fans, many=True)
    #    return Response(serializer.data)