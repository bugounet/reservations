from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Resource
from .forms import ResourceForm


class ResourcesListView(LoginRequiredMixin, ListView):
    model = Resource
    allow_empty = True
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
