from django.conf.urls import url, include
from apps.item.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^cambiar_estado/(?P<pk>\d+)/$', login_required(item_cambiar_estado), name='item_cambiar_estado'),
    url(r'^opciones/', login_required(item_opciones), name='item_opciones'),
    url(r'^crear/(?P<id_fase>\d+)/$', crear_item_basico, name='crear_item'),
    url(r'^importar_tipo_item/(?P<pk>\d+)/$', item_importar_ti, name='importar_tipo_item'),
    url(r'^atributos/(?P<pk>\d+)/$', item_set_atributos, name='set_atributos'),
    url(r'^lista/(?P<id_fase>\d+)/$', login_required(item_lista_fase), name='item_lista'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(item_eliminar), name='item_eliminar'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(item_modificar_basico), name='item_modificar'),
    # url(r'^editar_import_ti/(?P<pk>\d+)/$', login_required(ItemModificarImportTI.as_view()),
    #     name='item_modificar_import_ti'),
    url(r'^editar_import_ti/(?P<pk>\d+)/$', login_required(item_modificar_ti),
        name='item_modificar_import_ti'),
    url(r'^editar_atributos_ti/(?P<pk>\d+)/$', login_required(item_modificar_atributos),
        name='item_modificar_atr_ti'),
]
