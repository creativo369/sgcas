from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render

def role_required(allowed_roles=[]):

    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.roles in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
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
