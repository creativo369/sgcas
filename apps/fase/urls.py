from django.conf.urls import url
from apps.fase.views import *
from django.contrib.auth.decorators import login_required, permission_required
# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===

urlpatterns = [
    url(r'^opciones/', login_required(fase_opciones), name='fase_opciones'),
    url(r'^results/(?P<_id>\d+)/$', login_required(permission_required('fase.listar_fase', raise_exception=True)(search)), name='search'),
    url(r'^cambiar_estado/(?P<id_fase>\d+)/(?P<_id>\d+)/$', login_required(cambiar_estado_fase), name='fase_cambiar_estado'),
    url(r'^fase_detalles/(?P<id_fase>\d+)/$', login_required(fase_detalles), name='fase_detalles'),
    url(r'^crear/(?P<_id>\d+)/$', login_required(permission_required('fase.crear_fase',raise_exception=True)(FaseCrear.as_view())), name='crear_fase'),
    url(r'^lista/(?P<_id>\d+)/$', login_required(permission_required('fase.listar_fase', raise_exception=True)(lista_fase)), name='fase_lista'),
    url(r'^eliminar/(?P<id_fase>\d+)/(?P<_id>\d+)/$', login_required(eliminar_fase), name='fase_eliminar'),
    url(r'^editar/(?P<id_fase>\d+)/(?P<_id>\d+)/$', login_required(fase_modificar), name='fase_modificar'),
]

# **Volver atras** : [[forms.py]]

# **Ir a la documentación de vistas del modulo fase** : [[views.py]]

# === Indice de la documentación de la Aplicación fase  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)