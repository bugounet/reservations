from django.urls import path
from apps.website import views


urlpatterns = [
    path('', views.index_view, name="index"),
    path('logout', views.logout_view, name="logout"),
]
