from news import services
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class ReadMixin:

    @action(detail=True, methods=['post'], permission_classes=[
            permissions.IsAuthenticated])
    def read(self, request, pk=None):
        """Отмечает `obj` как прочитанный."""
        obj = self.get_object()
        services.add_read(obj, request.user)
        return Response()

    @action(detail=True, methods=['post'], permission_classes=[
            permissions.IsAuthenticated])
    def unread(self, request, pk=None):
        """Отмечает `obj` как не прочитанный."""
        obj = self.get_object()
        services.remove_read(obj, request.user)
        return Response()
