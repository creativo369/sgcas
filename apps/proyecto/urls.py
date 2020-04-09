from django.urls import path, include
from django.conf.urls import url

from apps.proyecto.views import home, success, CrearProyecto, \
ListaProyecto, ActualizarProyecto, EliminarProyecto

app_name='proyecto'

urlpatterns=[
	path('',home, name='home'),
	url(r'^crear-Proyecto/$', CrearProyecto.as_view(), name='crear_proyecto'),
	url(r'^listado_proyectos/$',ListaProyecto.as_view(), name='listado_proyecto'),
	url(r'^sucess/$',success,name='success'),
	url(r'^editar_proyecto/(?P<pk>\d+)/$',ActualizarProyecto.as_view(),name='editar_proyecto'),
	url(r'^eliminar_proyecto/(?P<pk>\d+)/$',EliminarProyecto.as_view(),name='eliminar_proyecto'),

]