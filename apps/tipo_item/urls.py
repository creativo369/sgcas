# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from apps.tipo_item.views import tipo_item_opciones, crear_tipo_item, eliminar_tipo_item, \
    editar_tipo_item, search, tipo_item_lista

# **Vistas basadas en clases**

# **1.Opciones :** Vista que despliega la gestión de tipo de item<br/>
# **2.Crear tipo item :** Vista que despliega la creación de un tipo de item<br/>
# **3.Listar tipo de item :** Vista que despliega la lista de tipo de item<br/>
# **4.Eliminar tipo de item :** Vista que despliega eliminar tipo de item<br/>
# **5.Editar tipo de item :** Vista que despliega edicion de un tipo de item<br/>
urlpatterns = [
    url(r'^opciones/', login_required(tipo_item_opciones), name='tipo_item_opciones'),
    url(r'^crear-tipo-item/(?P<id_fase>\d+)/$', login_required(crear_tipo_item), name='crear_tipo_item'),
    url(r'^lista-tipo-item/(?P<id_fase>\d+)/$', login_required(tipo_item_lista), name='tipo_item_lista'),
    url(r'^editar-tipo-item/(?P<pk>\d+)/$', login_required(editar_tipo_item), name='tipo_item_modificar'),
    url(r'^eliminar-tipo-item/(?P<pk>\d+)/$', login_required(eliminar_tipo_item), name='tipo_item_eliminar'),
    # url(r'^lista/(?P<id_fase>\d+)/$', login_required(permission_required('tipo_item.listar_tipo_item', raise_exception=True)(TipoItemLista.as_view())), name='tipo_item_lista'),)
    url(r'^results/$', login_required(search), name='search'),
    # url(r'^eliminar/(?P<pk>\d+)/$', login_required(permission_required('tipo_item.eliminar_tipo_item',raise_exception=True)(TipoItemEliminar.as_view())), name='tipo_item_eliminar'),)
    # url(r'^editar/(?P<pk>\d+)/$', login_required(permission_required('tipo_item.editar_tipo_item', raise_exception=True)(TipoItemModificar.as_view())), name='tipo_item_modificar'),
]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)