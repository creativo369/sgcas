# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===
from django.conf.urls import url
from apps.tipo_item.views import tipo_item_opciones, crear_tipo_item, TipoItemLista, TipoItemEliminar, \
    TipoItemModificar


# **Vistas basadas en clases**

# **1.Opciones :** Vista que despliega la gestión de tipo de item<br/>
# **2.Crear tipo item :** Vista que despliega la creación de un tipo de item<br/>
# **3.Listar tipo de item :** Vista que despliega la lista de tipo de item<br/>
# **4.Eliminar tipo de item :** Vista que despliega eliminar tipo de item<br/>
# **5.Editar tipo de item :** Vista que despliega edicion de un tipo de item<br/>
urlpatterns = [
    url(r'^opciones/', tipo_item_opciones, name='tipo_item_opciones'),
    url(r'^crear/', crear_tipo_item, name='crear_tipo_item'),
    url(r'^lista/', TipoItemLista.as_view(), name='tipo_item_lista'),
    url(r'^eliminar/(?P<pk>\d+)/$', TipoItemEliminar.as_view(), name='tipo_item_eliminar'),
    url(r'^editar/(?P<pk>\d+)/$', TipoItemModificar.as_view(), name='tipo_item_modificar'),
]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>
