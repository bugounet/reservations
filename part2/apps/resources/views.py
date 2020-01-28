from django.utils.timezone import now as tznow
from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly
from .models import Resource
from .serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminOrReadOnly]
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if instance.end_datetime < tznow():
            raise Exception("Oops!")
        instance.actions.cancel()
