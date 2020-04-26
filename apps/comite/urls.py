from django.urls import path, include
from django.conf.urls import url

from apps.comite.views import create, list, update, delete, success, detail, manage_comite

app_name = 'comite'
urlpatterns = [
    path('', manage_comite, name='manage_comite'),
    url(r'^crear-comite/$', create.as_view(), name='create'),
    url(r'^listado-comite/$', list.as_view(), name='list'),
    url(r'^editar-comite/(?P<pk>\d+)/$', update.as_view(), name='update'),
    url(r'^eliminar-comite/(?P<pk>\d+)/$', delete.as_view(), name='delete'),
    url(r'^operacion-exitosa/$', success, name='success'),
    url(r'^detalles-comite/(?P<pk>\d+)/$', detail.as_view(), name='detail'),
]
