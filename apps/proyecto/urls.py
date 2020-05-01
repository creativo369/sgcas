from django.urls import path, include
from django.conf.urls import url

from apps.proyecto.views import manage_projects, CreateProject, ListProject, UpdateProject, DeleteProject, \
    success, DetailProject, change_state

app_name = 'proyecto'
urlpatterns = [
    path('', manage_projects, name='manage_projects'),
    url(r'^crear-proyecto/$', CreateProject.as_view(), name='create'),
    url(r'^listado-proyecto/$', ListProject.as_view(), name='list'),
    url(r'^editar-proyecto/(?P<pk>\d+)/$', UpdateProject.as_view(), name='update'),
    url(r'^eliminar-proyecto/(?P<pk>\d+)/$', DeleteProject.as_view(), name='delete'),
    url(r'^detalles-proyecto/(?P<pk>\d+)/$', DetailProject.as_view(), name='detail'),
    url(r'^operacion-exitosa/$', success, name='success'),
    url(r'^transicion-proyecto/(?P<pk>\d+)/$', change_state, name='change'),
]
