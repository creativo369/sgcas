from django.conf.urls import url
from apps.fase.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^opciones/', login_required(fase_opciones), name='fase_opciones'),
    url(r'^cambiar_estado/(?P<pk>\d+)/(?P<_id>\d+)/$', login_required(cambiar_estado_fase), name='fase_cambiar_estado'),
    url(r'^fase_detalles/(?P<pk>\d+)/$', login_required(fase_detalles), name='fase_detalles'),
    url(r'^crear/(?P<_id>\d+)/$', FaseCrear.as_view(), name='crear_fase'),
    # url(r'^crear/(?P<_id>\d+)/$', crear_fase, name='crear_fase'),
    # url(r'^lista/(?P<_id>\d+)/$', login_required(FaseLista.as_view()), name='fase_lista'),
    url(r'^lista/(?P<_id>\d+)/$', lista_fase, name='fase_lista'),
    # url(r'^eliminar/(?P<pk>\d+)/(?P<_id>\d+)/$', login_required(FaseEliminar.as_view()), name='fase_eliminar'),
    url(r'^eliminar/(?P<pk>\d+)/(?P<_id>\d+)/$', eliminar_fase, name='fase_eliminar'),
    # url(r'^editar/(?P<pk>\d+)/$', login_required(FaseModificar.as_view()), name='fase_modificar'),
    url(r'^editar/(?P<pk>\d+)/(?P<_id>\d+)/$', login_required(fase_modificar), name='fase_modificar'),
]
