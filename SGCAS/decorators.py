from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from apps.fase.models import Fase
from apps.rol.models import Rol

##Checkea los permisos por fase
def requiere_permiso(permiso):
    def decorator(view_func):
        print("hola mundo")
        def wrap(request, *args, **kwargs):
            for rol_fase in Rol.objects.filter(fase=get_object_or_404(Fase, pk=kwargs.get('id_fase'))):
                if request.user in rol_fase.usuarios.all() and permiso in rol_fase.group.permissions.all():
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrap
    return decorator
    

def administrator_only(view_func):
    """

    :param view_func:
    :return:
    """
    def wrap(request, *args, **kwargs):
        if request.roles == 'Administrador':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


##Al crear un usuario, este no posee roles, por lo tanto se lo coloca como inactivo hasta que el admin
##active su cuenta
# def authorized_user(view_func):
#     def wrap(request, *args, **kwargs):
#         if request.roles:
#             return view_func(request, *args, **kwargs)
#         else:
#             return render(request, "base/unauthorized.html")
#
#     return wrap
