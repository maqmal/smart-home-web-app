"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from camera import views
from django.conf.urls import url
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('camera.urls')),
    path('catalog/', include('catalog.urls')),
    path('', views.index, name='index'),
    path('device_view/', views.index_device, name='index_device'),
    path('cam_view/', views.index_cam, name='index_cam'),
    path('camera/user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
