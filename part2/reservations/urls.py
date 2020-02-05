"""reservations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from .router import router as api_router
from django.contrib.auth import views as auth_views
from django.urls import path, include
from apps.website import urls as website_urls
from apps.booking.urls import urlpatterns as booking_urls
from apps.resources.urls import urlpatterns as resources_urls


urlpatterns = (
    i18n_patterns(
        path('admin/', admin.site.urls),
        path(
            'login',
            auth_views.LoginView.as_view(template_name='website/login.html'),
            name='login',
        ),
    ) +
    [
        path('api', include(api_router.urls)),
        path('', include(website_urls)),
        url(
            r'^social/',
            include('social.apps.django_app.urls', namespace='social')
        ),
    ]+
    booking_urls +
    resources_urls
)

