# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from SGCAS.decorators import requiere_permiso
from apps.rol.forms import GroupForm, GroupForm_sistema, RolFormUser
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from apps.rol.models import Rol
from apps.fase.models import Fase
from apps.usuario.models import User

"""
Todas las vistas para la aplicación del Modulo Rol
Actualmente se despliega en las plantillas 13 vistas:

1. **crear_rol_view** - funcion para la creación de roles por fase (Ir a la sección: [[views.py #crear rol]] )
2. **lista_rol** - Lista los roles existentes en la fase (Ir a la sección: [[views.py #listar roles]] )
3. **search** - lista los roles buscados dentro de la fase (Ir a la sección: [[views.py #search]] )
4. **editar_rol** - modifica los atributos de un rol de una fase (Ir a la sección: [[views.py #editar rol]] )
5. **eliminar_rol** - elimina un rol de la fase (Ir a la sección: [[views.py #eliminar rol]] )
6. **asignar_rol_usuario** - elimina un rol de la fase (Ir a la sección: [[views.py #asigna rol de fase]] )

7. **crear_rol_view_sistema** - funcion para la creación de roles de sistema (Ir a la sección: [[views.py #crear rol sistema]] )
8. **rol_opciones_sistema** - despliega opciones a sobre lo roles de sistema  (Ir a la sección: [[views.py #rol opciones sistema]] )
9. **lista_rol_sistema** - Lista los roles del sistema existentes (Ir a la sección: [[views.py #listar roles sistema]] )
10. **search_sistema** - lista los roles de sistema buscados (Ir a la sección: [[views.py #search sistema]] )
11. **editar_rol_sistema** - modifica los atributos de un rol de sistema (Ir a la sección: [[views.py #editar rol sistema]] )
12. **eliminar_rol_sistema** - elimina un rol de sistema (Ir a la sección: [[views.py #eliminar rol sistema]] )

13. **Usuario_roles** - lista los roles que posee el usuario actualmente (Ir a la sección: [[views.py #lista rol usuarios]] )
"""


# Vista que redefine la vista predeterminada del error 403.
def handler403(request, exception, template_name='403.html'):
    response = render(request, 'rol/403.html')
    response.status_code = 403
    return response


@login_required
@permission_required('rol.crear_rol', raise_exception=True)
# @requiere_permiso('crear_rol')
# === crear rol ===
def crear_rol_view(request, id_fase):
    """
    Permite la visualizacion de la plantilla para la creacion de instancias del modelo Rol.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe el id de la fase donde se desea crear el rol.<br/>
    **:return:** Se almacena una instancia del modelo Rol.<br/>
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            rol = Rol.objects.create(nombre=group.name, group=group, fase=get_object_or_404(Fase, id=id_fase))
            return redirect('rol:rol_lista', id_fase=id_fase)
    else:
        form = GroupForm()
    return render(request, 'rol/rol_crear.html', {'form': form})


@permission_required('rol.listar_rol', raise_exception=True)
# @requiere_permiso('listar_rol')
# === listar roles ===
def lista_rol(request, id_fase):
    """
     Permite la visualizacion de todas las intancias del modelo Rol existentes en la fase.<br/>
     **:param request:** Recibe un request por parte un usuario.<br/>
     **:param id_fase:** Recibe el id de la fase cuyos roles se desean visualizar.<br/>
     **:return:** Lista que contiene todas las instancias del modelo Rol de la fase.<br/>
    """
    rol = Rol.objects.filter(fase=get_object_or_404(Fase, pk=id_fase)).order_by('id').distinct()
    paginator = Paginator(rol, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'rol/rol_lista.html', {'fase': Fase.objects.get(id=id_fase),
                                                   'proyecto': Fase.objects.get(id=id_fase).proyecto,
                                                  'page_obj': page_obj})


# @requiere_permiso('listar_rol')
@permission_required('rol.listar_rol', raise_exception=True)
# === search ===
def search(request, id_fase):
    """
    Permite la búsqueda de las intancias del modelo Rol.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/> 
    **:param id_fase:** Recibe el id de la fase cuyos roles se desean buscarse.<br/>   
    **:return:** Lista todas las instancias del modelo Rol que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'rol/list_busqueda.html'
    query = request.GET.get('buscar')

    if query:
        results = Rol.objects.filter(Q(fase=get_object_or_404(Fase, pk=id_fase))
                                     & Q(nombre__icontains=query)).order_by('id').distinct()
    else:
        results = Rol.objects.filter(Q(fase=get_object_or_404(Fase, pk=id_fase))).order_by('id').distinct()

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template, {'fase': Fase.objects.get(id=id_fase),'proyecto':Fase.objects.get(id=id_fase).proyecto,
                                      'page_obj': page_obj})


# @requiere_permiso('editar_rol')
@permission_required('rol.editar_rol', raise_exception=True)
# === editar rol ===
def editar_rol(request, pk, id_fase):
    """
     Permite la modificación de una instancia del modelo Rol.<br/>
     **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la instancia del modelo Rol que se desea editar.<br/>
     **:return:** Se modifica la instancia del modelo Rol referenciado y se regresa a la lista de roles de la fase.<br/>
    """
    rol = get_object_or_404(Rol, id=pk)
    group = rol.group
    # id_fase = rol.fase.id
    form = GroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group = form.save()
        rol.group = group
        return redirect('rol:rol_lista', id_fase=id_fase)
    return render(request, 'rol/rol_editar.html', {'form': form, 'fase': Fase.objects.get(id=id_fase)})


# @requiere_permiso('eliminar_rol')
@permission_required('rol.eliminar_rol', raise_exception=True)
# === eliminar rol ===
def eliminar_rol(request, pk, id_fase):
    """
     Permite la eliminación de una instancia del modelo Rol.<br/>
     **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la instancia del modelo Rol que se desea eliminar de la fase.<br/>
     **:return:** Se elimina la instancia del modelo Rol referenciado y se regresa a la lista de roles de la fase.<br/>
    """
    rol = get_object_or_404(Rol, id=pk)
    # id_fase = rol.fase.pk
    if len(rol.usuarios.all()) == 0:
        # rol.delete()
        Group.objects.get(name=rol.nombre).delete()
        return redirect('rol:rol_lista', id_fase=id_fase)
    else:
        return render(request, 'rol/validate_delete.html')


# === asigna rol de fase
# @requiere_permiso('asignar_rol')
@permission_required('rol.asignar_rol', raise_exception=True)
def asignar_rol_usuario(request, pk, id_fase):
    rol = get_object_or_404(Rol, pk=pk)
    # id_fase = rol.fase.id
    form = RolFormUser(request.POST or None, instance=rol)
    if form.is_valid():
        rol = form.save()

        for user in rol.usuarios.all():
            user.groups.add(rol.group)

        return redirect('rol:rol_lista', id_fase=id_fase)
    return render(request, 'rol/rol_asignar_usuario.html', {'form': form, 'role': rol})


# === ROL POR SISTEMA ===

@login_required
@permission_required('rol.crear_rol_sistema', raise_exception=True)
# === crear rol sistema ===
def crear_rol_view_sistema(request):
    """
    Permite la visualizacion de la plantilla para la creacion de instancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Se almacena una instancia del modelo Group.<br/>
    """
    if request.method == 'POST':
        form = GroupForm_sistema(request.POST)
        if form.is_valid():
            group = form.save()
            rol = Rol.objects.create(nombre=group.name, group=group, fase=None)
        return redirect('rol:rol_lista_sistema')
    else:
        form = GroupForm_sistema()
    return render(request, 'rol/rol_crear_sistema.html', {'form': form})


@login_required
@permission_required('rol.gestion_rol_sistema', raise_exception=True)
# === rol opciones sistema ===
def rol_opciones_sistema(request):
    """
    Permite la visualizacion de las opciones sobre el modelo Group.<br/>
    **:param request:** Recibe un request por parte un usuario.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
    """
    return render(request, 'rol/rol_opciones_sistema.html')


# === listar roles sistema ===
class ListaRol_sistema(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion de todas las intancias del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
    """
    paginate_by = 3
    model = Rol
    template_name = 'rol/rol_lista_sistema.html'
    permission_required = 'rol.listar_rol_sistema'

    # La lista a mostrar estara por orden ascendente
    # class Meta:
    # ordering = ['-id']
    def get_queryset(self):
        # Rol.objects.filter(fase=None)
        return Rol.objects.filter(fase=None).order_by('id').distinct()


@permission_required('rol.listar_rol_sistema', raise_exception=True)
# === search sistema ===
def search_sistema(request):
    """
    Permite la búsqueda de las intancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Lista todas las instancias del modelo Group que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'rol/list_busqueda_sistema.html'
    query = request.GET.get('buscar')

    if query:
        results = Rol.objects.filter(Q(nombre__icontains=query), fase=None).order_by('id').distinct()
    else:
        results = Rol.objects.filter(fase=None).order_by('id')

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template, {'page_obj': page_obj})


# === editar rol sistema ===
class EditarRol_sistema(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de una instancia del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Se modifica la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
    """
    model = Group
    form_class = GroupForm_sistema
    permission_required = 'rol.editar_rol_sistema'
    template_name = 'rol/rol_editar_sistema.html'
    success_url = reverse_lazy('rol:rol_lista_sistema')


# === eliminar rol sistema ===
class EliminarRol_sistema(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo Rol.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Se elimina la instancia del modelo Rol referenciado y se regresa a la lista de roles del sistema.<br/>
    """
    model = Rol
    template_name = 'rol/rol_eliminar_sistema.html'
    permission_required = 'rol.eliminar_rol_sistema'
    success_url = reverse_lazy('rol:rol_lista_sistema')

    def post(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')  # se obtiene el pk para eliminar
        rol = Rol.objects.get(pk=pk)
        if not len(rol.usuarios.all()) == 0:
            return render(request, 'rol/validate_delete.html')
        else:
            Group.objects.get(name=rol.nombre).delete()
            # rol.delete()
            return redirect(self.success_url)

        # === lista rol usuarios ===


class Usuario_roles(ListView):
    """
    Permite la visualizacion de todas las intancias del modelo Rol que posee un usuario.<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Rol que pertenecen a un usuario.<br/>
    """
    model = Rol
    template_name = 'rol/usuario_roles.html'

    def get(self, request, *args, **kwargs):
        rol = Rol.objects.filter(usuarios__in=User.objects.filter(id=request.user.id))
        print(rol.exists())
        if rol.exists():
            return render(request, self.template_name, {'rol': rol})
        return render(request, self.template_name, {'rol': rol})

# === FIN ====

# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>


# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
