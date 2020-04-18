"""weeklygoal URL Configuration

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
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from weeklygoal.apps.activities import views as api

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    path("filer/", include("filer.urls")),
    # Authentication
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # API
    path("api/event/create", api.create_event, name="create_event"),
    path("api/event/delete/<int:event_id>", api.delete_event, name="delete_event"),
    path("api/week/<str:direction>", api.change_week, name="change_week"),
    # Frontend
    path("app/", api.app, name="app"),
    path("", api.app, name="app"),
]

# Serve uploaded images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = api.redirect_to_app
