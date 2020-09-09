from django.urls import path, include
from django.conf.urls import url


from django.contrib.auth.decorators import login_required, permission_required
from apps.proyecto.views import manage_projects, CreateProject, ListProject, UpdateProject, DeleteProject, \
    success, DetailProject, change_state, search

app_name = 'proyecto'
# ** Dirección de URL desplegar las vistas en la dirección de plantillas respectivamente. **
urlpatterns = [
    path('', manage_projects, name='manage_projects'),
    url(r'^crear-proyecto/$', login_required(permission_required('proyecto.crear_proyecto', raise_exception=True)(CreateProject.as_view())), name='create'),
    url(r'^listado-proyecto/$', login_required(permission_required('proyecto.ver_proyecto', raise_exception=True)(ListProject.as_view())), name='list'),
    url(r'^results/$', login_required(permission_required('proyecto.ver_proyecto', raise_exception=True)(search)), name='search'),
    url(r'^editar-proyecto/(?P<pk>\d+)/$', login_required(permission_required('proyecto.editar_proyecto', raise_exception=True)(UpdateProject.as_view())), name='update'),
    url(r'^eliminar-proyecto/(?P<pk>\d+)/$', login_required(permission_required('proyecto.eliminar_proyecto', raise_exception=True)(DeleteProject.as_view())), name='delete'),
    url(r'^detalles-proyecto/(?P<pk>\d+)/$', login_required(permission_required('proyecto.detalles_proyecto', raise_exception=True)(DetailProject.as_view())), name='detail'),
    url(r'^operacion-exitosa/$', login_required(success), name='success'),
    url(r'^transicion-proyecto/(?P<pk>\d+)/$', login_required(change_state), name='change'),
]


# **Volver atras** : [[tests.py]]

# **Ir a la documentación de vistas de la Aplicación** :[[views.py]]

# === Indice de la documentación de la Aplicación Proyecto  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)