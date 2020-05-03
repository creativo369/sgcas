from django.conf.urls import url, include
from apps.linea_base.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^agregar_item_lb/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(agregar_items_lb), name='agregar_items_lb'),
    url(r'^crear/(?P<id_fase>\d+)/$', login_required(crear_linea_base), name='crear_linea'),
    url(r'^editar_linea_base/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(editar_lb), name='editar_lb'),
    url(r'^lista/(?P<id_fase>\d+)/$', login_required(lista_linea_base), name='linea_lista'),
    url(r'^lista_items/(?P<pk>\d+)/$', login_required(lista_items_linea_base), name='linea_items_lista'),
    url(r'^cambiar_estado_lb/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(estado_lb), name='linea_estado'),
    url(r'^eliminar_lb/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(eliminar_lb), name='eliminar_lb'),
    # url(r'^editar/(?P<pk>\d+)/$', login_required(LineaModificar.as_view()), name='linea_modificar'),
]
