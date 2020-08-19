from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===

# **Vistas basadas en clases**

# **1.CreateComite :** Vista que despliega la creación de un comité<br/>
# **2.UpdateComite :** Vista que despliega la modificación de un comité<br/>
# **3.DeleteComite :** Vista que despliega eliminar un comité<br/>
from apps.comite.views import CreateComite, UpdateComite, DeleteComite, success

app_name = 'comite'
# ** Dirección de URL desplegar las vistas en la dirección de plantillas respectivamente. **
urlpatterns = [
    url(r'^crear-comite/(?P<_id>\d+)/$', login_required(permission_required('comite.crear_comite', raise_exception=True)(CreateComite.as_view())), name='create'),
    url(r'^editar-comite/(?P<pk>\d+)/$', login_required(permission_required('comite.editar_comite', raise_exception=True)(UpdateComite.as_view())), name='update'),
    url(r'^eliminar-comite/(?P<pk>\d+)/$', login_required(permission_required('comite.eliminar_comite', raise_exception=True)(DeleteComite.as_view())), name='delete'),
    url(r'^operacion-exitosa/$', login_required(success), name='success'),
]

# **Atras** : [[tests.py]]

# **Siguiente** : [[views.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
