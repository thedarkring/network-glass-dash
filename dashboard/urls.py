from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.urls import path
from .views import dashboard, devices, search

urlpatterns = [
    path('', dashboard.DashboardView.as_view(), name="dashboard"),
    url(r'^api$', search.DeviceApi.as_view(), name="device-api"),
    url(r'^admin/', admin.site.urls),
    url(r'^multi_device', devices.DeviceView.as_view(), name="multi_device"),
]
