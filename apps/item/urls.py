from django.conf.urls import url
from apps.item.views import *
from django.contrib.auth.decorators import login_required

# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===

# **Vistas : **

# **1.Cambiar estado de un item :** Vista que despliega el cambio de estado de un item<br/>
# **2.Gestión de items          :** Vista que despliega la gestión de items<br/>
# **3.Crea item                 :** Vista que despliega la creación de un item<br/>
# **4.Importar tipo de item     :** Vista que despliega los tipos de items para importarlos<br/>
# **5.Atributos de un tipo_item :** Vista que despliega los atributos para un tipo de item<br/>
# **6.Listar items              :** Vista que despliega la lista de items en una fase<br/>
# **7.Eliminar item             :** Vista que despliega eliminar un item<br/>
# **8.Editar                    :** Vista que despliega editar un item<br/>
# **9.Editar tipo de item       :** Vista que despliega editar un tipo de item<br/>
# **10.Editar atributos         :** Vista que despliega editar los datos de un atributo de un tipo_item<br/>


# ** Dirección de URL desplegar las vistas en la dirección de plantillas respectivamente. **
urlpatterns = [
    url(r'^cambiar_estado/(?P<pk>\d+)/$', login_required(item_cambiar_estado), name='item_cambiar_estado'),
    url(r'^item_detalles/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(item_detalles), name='item_detalles'),
    url(r'^versiones/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(item_versiones), name='versiones'),
    url(r'^calculo-de-impacto/(?P<pk>\d+)/$', login_required(calculo_impacto), name='calculo_impacto'),
    url(r'^trazabilidad-de-item/(?P<pk>\d+)/$', login_required(trazabilidad), name='trazabilidad'),
    url(r'^restaurar_version/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(restaurar_version),
        name='restaurar_version'),
    url(r'^fases_relaciones/(?P<pk>\d+)/$', login_required(fases_rel), name='fases_rel'),
    url(r'^relaciones/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(relaciones), name='relaciones'),
    url(r'^crear/(?P<id_fase>\d+)/$', login_required(crear_item_basico), name='crear_item'),
    url(r'^importar_tipo_item/(?P<pk>\d+)/$', login_required(item_importar_ti), name='importar_tipo_item'),
    url(r'^atributos/(?P<pk>\d+)/$', login_required(item_set_atributos), name='set_atributos'),
    url(r'^results/(?P<id_fase>\d+)/$', login_required(search), name='search'),
    url(r'^lista/(?P<id_fase>\d+)/$', login_required(item_lista_fase), name='item_lista'),
    url(r'^eliminar/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(item_eliminar), name='item_eliminar'),
    url(r'^editar/(?P<pk>\d+)/(?P<id_fase>\d+)/$', login_required(item_modificar_basico), name='item_modificar'),
    url(r'^editar_import_ti/(?P<pk>\d+)/$', login_required(item_modificar_ti), name='item_modificar_import_ti'),
    url(r'^editar_atributos_ti/(?P<pk>\d+)/$', login_required(item_modificar_atributos), name='item_modificar_atr_ti'),
]
# **Atras** : [[tests.py]]

# **Siguiente** : [[views.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
