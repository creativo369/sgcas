from django.urls import path, include
from django.conf.urls import url

from apps.comite.views import CreateComite, UpdateComite, DeleteComite, success

app_name = 'comite'
urlpatterns = [
    url(r'^crear-comite/(?P<_id>\d+)/$', CreateComite.as_view(), name='create'),
    url(r'^editar-comite/(?P<pk>\d+)/$', UpdateComite.as_view(), name='update'),
    url(r'^eliminar-comite/(?P<pk>\d+)/$', DeleteComite.as_view(), name='delete'),
    url(r'^operacion-exitosa/$', success, name='success'),
]
