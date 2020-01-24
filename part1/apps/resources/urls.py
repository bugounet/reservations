from django.urls import path
from .views import ResourcesListView, ResourceCreationView

urlpatterns = [
    path(
        'new-resource',
        ResourceCreationView.as_view(),
        name="create_resource_view"
    ),
    path('resources', ResourcesListView.as_view(), name="resources_list"),
]
