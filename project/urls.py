"""project URL Configuration

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
from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static

from base import views as base_views

urlpatterns = [
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('regions/', include('regions.urls')),
    path('status/', base_views.StatusView.as_view(), name='status'),
    path('api/v1/', include('api.urls', namespace='api')),
    path('', base_views.index, name='home'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

# custom error pages
handler400 = 'base.views.bad_request_view'
handler403 = 'base.views.permission_denied_view'
handler404 = 'base.views.page_not_found_view'
handler500 = 'base.views.server_error_view'
