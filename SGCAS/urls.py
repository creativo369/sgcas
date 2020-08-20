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

from django.conf.urls import url, handler403
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView
from SGCAS.settings import base, desarrollo
# from django.contrib.auth.views import logout_then_login


handler403 = 'apps.rol.views.handler403'
# se asigna la nueva ruta de la vista creada para el error 403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="account/index.html")),
    url(r'^account/', include('allauth.urls')),
    path('usuario/', include('apps.usuario.urls', namespace='usuario')),
    path('rol/', include(('apps.rol.urls', 'rol'), namespace='rol')),
    path('item/', include(('apps.item.urls', 'item'), namespace='item')),
    path('tipo_item/', include(('apps.tipo_item.urls', 'tipo_item'), namespace='tipo_item')),
    path('mensajes/', include(('apps.mensajes.urls', 'mensajes'), namespace='mensajes')),
    path('gestion-proyecto/', include(('apps.proyecto.urls', 'proyecto'), namespace='proyecto')),
    path('comite/', include(('apps.comite.urls', 'comite'), namespace='comite')),
    path('fase/', include(('apps.fase.urls', 'fase'), namespace='fase')),
    url(r'^faq/', login_required(TemplateView.as_view(template_name='faq.html'))),
    path('linea_base/', include(('apps.linea_base.urls', 'linea_base'), namespace='linea_base')),
]

if desarrollo.DEBUG:
    urlpatterns += static(desarrollo.MEDIA_URL, document_root=desarrollo.MEDIA_ROOT)
    # urlpatterns += static(desarrollo.STATIC_URL, document_root=base.STATIC_ROOT)

"""
    path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="account_login"),
<<<<<<< HEAD
    path('logout/', views.logout, name="account_logout"),
=======
    path("logout/", views.logout, name="account_logout"),
>>>>>>> origin/guillermo
    path("password/change/", views.password_change,
         name="account_change_password"),
    path("password/set/", views.password_set, name="account_set_password"),
    path("inactive/", views.account_inactive, name="account_inactive"),

    # E-mail
    path("email/", views.email, name="account_email"),
    path("confirm-email/", views.email_verification_sent,
         name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email,
            name="account_confirm_email"),

    # password reset
    path("password/reset/", views.password_reset,
         name="account_reset_password"),
    path("password/reset/done/", views.password_reset_done,
         name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", views.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
"""
