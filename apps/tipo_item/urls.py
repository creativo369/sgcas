from django.conf.urls import url, include
from apps.tipo_item.views import tipo_item_opciones, crear_tipo_item, TipoItemLista, TipoItemEliminar

urlpatterns = [
	url(r'^opciones/', tipo_item_opciones, name = 'tipo_item_opciones'),
	url(r'^crear/', crear_tipo_item, name = 'crear_tipo_item'),
	url(r'^lista/', TipoItemLista.as_view(), name = 'tipo_item_lista'),
    url(r'^eliminar/(?P<pk>\d+)/$',TipoItemEliminar.as_view(), name = 'tipo_item_eliminar'),
]
