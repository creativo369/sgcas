"""SGCAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from apps.login.views import login_view
from apps.usuario.views import usuario_view

from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', login_view),
    path('account/', include('apps.usuario.urls', namespace = 'usuario')),
    path('logout/',logout_then_login, name = "logout"),
    path('rol/', include(('apps.rol.urls', 'rol'), namespace = 'rol')),
]
