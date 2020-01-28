from django.utils.timezone import now as tznow
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets

from .forms import ResourceForm
from .models import Resource
from .permissions import IsAdminOrReadOnly
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


class ResourcesListView(LoginRequiredMixin, ListView):
    model = Resource
    allow_empty = True
    paginate_by = 10
    template_name = 'resources/resources_list.html'


class AdminLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ResourceCreationView(AdminLoginRequiredMixin, CreateView):
    model = Resource
    template_name = 'resources/resource_create.html'
    form_class = ResourceForm
    context_object_name = 'resource'

    @property
    def success_url(self):
        return reverse('resources_list')

    def get_queryset(self):
        return Resource.objects.for_user(self.request.user)

class ResourceDetailsView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = 'resources/resource_details.html'
