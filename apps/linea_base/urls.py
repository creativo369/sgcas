# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===
from django.conf.urls import url
from apps.linea_base.views import *
from django.contrib.auth.decorators import login_required


# **Vistas :**

# **1.Agregar item a la linea base  :** Vista que despliega la opción de incluir/excluir un item de una linea base<br/>
# **2.Crear linea base              :** Vista que despliega la creación de una linea base<br/>
# **3.Editar Linea base             :** Vista que despliega la edición de una linea base<br/>
# **4.Listar las lineas bases       :** Vista que despliega el listado de lineas base<br/>
# **5.Listar los items de una lb    :** Vista que despliega el listado de items de una linea base<br/>
# **6.cambiar el estado lb          :** Vista que despliega el cambio de un estado de linea base<br/>
# **7.Eliminar la linea base        :** Vista que despliega eliminar una linea base<br/>
# ** Dirección de URL desplegar las vistas en la dirección de plantillas respectivamente. **
urlpatterns = [
    url(r'^agregar_item_lb/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(agregar_items_lb), name='agregar_items_lb'),
    url(r'^crear/(?P<id_fase>\d+)/$', login_required(crear_linea_base), name='crear_linea'),
    url(r'^editar_linea_base/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(editar_lb), name='editar_lb'),
    url(r'^lista/(?P<id_fase>\d+)/$', login_required(lista_linea_base), name='linea_lista'),
    url(r'^lista_items/(?P<pk>\d+)/$', login_required(lista_items_linea_base), name='linea_items_lista'),
    url(r'^cambiar_estado_lb/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(estado_lb), name='linea_estado'),
    url(r'^eliminar_lb/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(eliminar_lb), name='eliminar_lb'),
]

# **Volver atras** : [[apps.py]]

# **Ir a la documentación del vistas de la linea base** : [[views.py]]

# === Indice de la documentación de la Aplicación linea base  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>
