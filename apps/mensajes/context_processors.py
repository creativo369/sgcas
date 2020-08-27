from apps.usuario.models import User


def count_inactive_users(request):
    """
    Función que cuenta la cantidad de usuarios inactivos dentro del sistema.<br/>
    **:param request:** la solicitud del cliente url <br/>
    **:return:** la cantidad de usuarios inactivos en el sistema. <br/>
    """
    total_users = User.objects.all().exclude(username='AnonymousUser')
    inactive_users = 0
    for user in total_users:
        if not user.is_active:
            inactive_users = inactive_users + 1
    return {'count_inactive_users': inactive_users}
# **Volver atras** :[[apps.py]]
# **Ir a la documentación del tests de la Aplicación** :[[forms.py]]

# === Indice de la documentación de la Aplicación mensajes  === <br/>
# 1.apps                : [[apps.py]]<br/>
# 2.context_processors  : [[context_processors.py]]<br/>
# 3.test                : [[tests.py]]<br/>
# 4.urls                : [[urls.py]]<br/>
# 5.views               : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
