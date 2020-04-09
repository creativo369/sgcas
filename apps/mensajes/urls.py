from django.conf.urls import url
from apps.mensajes.views import Mensajes, ActualizarUsuarioMensaje, EliminarUsuarioMensaje

urlpatterns = [
    url(r'^lista/', Mensajes.as_view(), name='mensaje_lista'),
    url(r'^modificar/(?P<pk>\d+)/$', ActualizarUsuarioMensaje.as_view(), name='mensaje_usuario_modificar'),
    url(r'^eliminar/(?P<pk>\d+)/$', EliminarUsuarioMensaje.as_view(), name='mensaje_usuario_eliminar'),

]
