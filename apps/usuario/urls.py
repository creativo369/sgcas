from django.conf.urls import url
from django.urls import path
# === Importamos las vistas basadas en clases y en funciones del codigo fuente de views.py ===
from apps.usuario.views import usuario_opciones, usuario_view, UsuarioLista, RegistrarUsuario, ActualizarUsuario, \
    EliminarUsuario

app_name='administracion'
# ** Vistas: **

# **1.Usuario Lobby :** Vista que despliega un espacio para el usuario registrado en el sistema<br/>
# **2.Gestión de Usuarios :** Vista que despliega la gestión de usuarios<br/>
# **3.Lista de Usuarios :** Vista que despliega la lista de usuarios<br/>
# **4.Registrar un usuario :** Vista que despliega el registro de usuarios<br/>
# **5.editar un usuario :** Vista que despliega la edición de usuarios<br/>
# **6.eliminar un usuario :** Vista que despliega la eliminación de usuarios<br/>
urlpatterns= (
    path('', usuario_view, name='usuario_home'),
    url(r'^usuario_opciones/', usuario_opciones, name='usuario_opciones'),
    url(r'^lista/', UsuarioLista.as_view(), name='usuario_lista'),
    url(r'^registrar/', RegistrarUsuario.as_view(), name="usuario_registrar"),
    url(r'^editar/(?P<pk>\d+)/$',ActualizarUsuario.as_view(), name='usuario_editar'),
    url(r'^eliminar/(?P<pk>\d+)/$',EliminarUsuario.as_view(), name='usuario_eliminar'),
)

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>