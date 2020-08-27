# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from apps.rol.views import crear_rol_view, rol_opciones, ListaRol, EditarRol, EliminarRol, search

# **Vistas**

# **1.Opciones :** Vista que despliega la gestión de roles<br/>
# **2.lista :** Vista que despliega la lista de roles existentes en el sistema<br/>
# **3.eliminar rol :** Vista que despliega eliminar un rol<br/>
# **4.crear rol :** Vista que despliega la definición de un rol<br/>
# **5.modificar rol :** Vista que despliega modificar un rol<br/>
urlpatterns = [
    # ** Dirección de URL desplegar las vistas en la dirección de plantillas respectivamente. **
    url(r'^opciones/', login_required(rol_opciones), name='rol_opciones'),
    url(r'^lista/', login_required(ListaRol.as_view()), name='rol_lista'),
    url(r'^results/$', login_required(search), name='search'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(EliminarRol.as_view()), name='rol_eliminar'),
    url(r'^crear/', login_required(crear_rol_view), name='rol_crear'),
    url(r'^modificar/(?P<pk>\d+)/$', login_required(EditarRol.as_view(model=Group, )), name='rol_editar'),
]

# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)