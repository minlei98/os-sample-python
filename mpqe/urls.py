"""mpqe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^mpqe/api/', include('api.urls')),
    
    # mpqe admin
    path('mpqe/', admin.site.urls),
    path('mpqe/', include('dashboard.urls')),
]
 
admin.site.site_header = "MPTS Management"
admin.site.site_title = "MPTS-Portal"
admin.site.index_title = "Administration" 
admin.site.list_per_page = 10
admin.site.site_url = 'http://redhat.com/'
admin.empty_value_display = '**Empty**'

