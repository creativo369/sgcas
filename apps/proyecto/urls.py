from django.urls import path, include
from django.conf.urls import url

from apps.proyecto.views import manage_projects, create, list, update, delete, success, detail

app_name='proyecto'
urlpatterns=[
	path('',manage_projects, name='manage_projects'),
	url(r'^crear-proyecto/$', create.as_view(), name='create'),
	url(r'^listado-proyecto/$',list.as_view(), name='list'),
	url(r'^editar-proyecto/(?P<pk>\d+)/$',update.as_view(),name='update'),
	url(r'^eliminar-proyecto/(?P<pk>\d+)/$',delete.as_view(),name='delete'),
	url(r'^operacion-exitosa/$',success,name='success'),
	url(r'^detalles-proyecto/(?P<pk>\d+)/$',detail.as_view(),name='detail'),
]