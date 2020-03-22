from django.conf.urls import url, include
from django.contrib.auth.models import Group
from apps.rol.views import crear_rol_view, rol_opciones, ListaRol, EditarRol, EliminarRol

urlpatterns = [
	url(r'^opciones/', rol_opciones, name = 'rol_opciones'),
	url(r'^lista/', ListaRol.as_view(),name = 'rol_lista'),
    url(r'^eliminar/(?P<pk>\d+)/$',EliminarRol.as_view(),name = 'rol_eliminar'),
    url(r'^crear/', crear_rol_view, name = 'rol_crear'),
    url(r'^modificar/(?P<pk>\d+)/$', EditarRol.as_view(model = Group,), name = 'rol_editar'),
]

