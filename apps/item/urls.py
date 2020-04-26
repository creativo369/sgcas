from django.conf.urls import url, include
from apps.item.views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    url(r'^opciones/', login_required(item_opciones), name='item_opciones'),
    url(r'^crear/', ItemCrear.as_view(), name='crear_item'),
    url(r'^importar_tipo_item/(?P<pk>\d+)/$', ImportarTipoItem.as_view(), name='importar_tipo_item'),
    url(r'^atributos/(?P<pk>\d+)/$', SetAtributos.as_view(), name='set_atributos'),
    url(r'^lista/', login_required(ItemLista.as_view()), name='item_lista'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(ItemEliminar.as_view()), name='item_eliminar'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(ItemModificar.as_view()), name='item_modificar'),
    url(r'^editar_import_ti/(?P<pk>\d+)/$', login_required(ItemModificarImportTI.as_view()), name='item_modificar_import_ti'),
    url(r'^editar_atributos_ti/(?P<pk>\d+)/$', login_required(ItemModificarAtrTI.as_view()), name='item_modificar_atr_ti'),
]
