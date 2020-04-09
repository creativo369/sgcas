from django.conf.urls import url
from django.urls import path

from apps.usuario.views import usuario_opciones, usuario_view, UsuarioLista, RegistrarUsuario, ActualizarUsuario, \
    EliminarUsuario

app_name='administracion'

urlpatterns= (
    path('', usuario_view, name='usuario_home'),
    url(r'^usuario_opciones/', usuario_opciones, name='usuario_opciones'),
    url(r'^lista/', UsuarioLista.as_view(), name='usuario_lista'),
    url(r'^registrar/', RegistrarUsuario.as_view(), name="usuario_registrar"),
    url(r'^editar/(?P<pk>\d+)/$',ActualizarUsuario.as_view(), name='usuario_editar'),
    url(r'^eliminar/(?P<pk>\d+)/$',EliminarUsuario.as_view(), name='usuario_eliminar'),
)
