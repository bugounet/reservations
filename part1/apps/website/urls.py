from django.urls import path
from django.contrib.auth import views as auth_views

from apps.website import views
from apps.booking.urls import urlpatterns as booking_urls
urlpatterns = [
    path('', views.index_view, name="index"),
    path('logout', views.logout_view, name="logout"),
    path(
        'login',
        auth_views.LoginView.as_view(template_name='website/login.html'),
        name='login',
    ),
] + booking_urls
