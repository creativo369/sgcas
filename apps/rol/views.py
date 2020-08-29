# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rol.forms import GroupForm, GroupForm_sistema
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from apps.rol.models import Rol
from apps.fase.models import Fase

"""
Todas las vistas para la aplicación del Modulo Rol
Actualmente se despliega en las plantillas 5 vistas:

1. **crear_rol_view** - funcion para la creación de roles  (Ir a la sección: [[views.py #crear rol]] )
2. **lista_rol** - Lista los roles existentes (Ir a la sección: [[views.py #listar roles]] )
3. **search** - lista los roles buscados (Ir a la sección: [[views.py #search]] )
4. **editar_rol** - modifica los atributos de un rol (Ir a la sección: [[views.py #editar rol]] )
5. **eliminar_rol** - elimina un rol (Ir a la sección: [[views.py #eliminar rol]] )
"""


# Vista que redefine la vista predeterminada del error 403.
def handler403(request, exception, template_name='403.html'):
    response = render(request, 'rol/403.html')
    response.status_code = 403
    return response


@login_required
@permission_required('usuario.crear_rol', raise_exception=True)
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
            rol = Rol.objects.create(nombre=group.name, group=group, fase=get_object_or_404(Fase, pk=id_fase))
            return redirect('rol:rol_lista', id_fase=id_fase)
    else:
        form = GroupForm()
    return render(request, 'rol/rol_crear.html', {'form': form})


@permission_required('usuario.listar_rol', raise_exception=True)
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
                                                  'page_obj': page_obj})


@permission_required('usuario.listar_rol', raise_exception=True)
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

    return render(request, template, {'fase': Fase.objects.get(id=id_fase), 'page_obj': page_obj})


@permission_required('usuario.editar_rol', raise_exception=True)
# === editar rol ===
def editar_rol(request, pk):
    """
     Permite la modificación de una instancia del modelo Rol.<br/>
     **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la instancia del modelo Rol que se desea editar.<br/>
     **:return:** Se modifica la instancia del modelo Rol referenciado y se regresa a la lista de roles de la fase.<br/>
    """
    rol = get_object_or_404(Rol, pk=pk)
    group = rol.group
    id_fase = rol.fase.id
    form = GroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group = form.save()
        rol.group = group
        return redirect('rol:rol_lista', id_fase=id_fase)
    return render(request, 'rol/rol_editar.html', {'form': form, 'fase': Fase.objects.get(id=id_fase)})


@permission_required('usuario.eliminar_rol', raise_exception=True)
# === eliminar rol ===
def eliminar_rol(request, pk):
    """
     Permite la eliminación de una instancia del modelo Rol.<br/>
     **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la instancia del modelo Rol que se desea eliminar de la fase.<br/>
     **:return:** Se elimina la instancia del modelo Rol referenciado y se regresa a la lista de roles de la fase.<br/>
    """
    rol = get_object_or_404(Rol, pk=pk)
    id_fase = rol.fase.pk
    rol.delete()
    return redirect('rol:rol_lista', id_fase=id_fase)


# === ROL POR SISTEMA ===

@login_required
@permission_required('usuario.crear_rol_sistema', raise_exception=True)
# === crear rol ===
def crear_rol_view_sistema(request):
    """
    Permite la visualizacion de la plantilla para la creacion de instancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Se almacena una instancia del modelo Group.<br/>
    """
    if request.method == 'POST':
        form = GroupForm_sistema(request.POST)
        if form.is_valid():
            form.save()
        return redirect('rol:rol_lista_sistema')
    else:
        form = GroupForm_sistema()
    return render(request, 'rol/rol_crear_sistema.html', {'form': form})


@login_required
@permission_required('usuario.ver_rol_sistema', raise_exception=True)
# === rol opciones ===
def rol_opciones_sistema(request):
    """
    Permite la visualizacion de las opciones sobre el modelo Group.<br/>
    **:param request:** Recibe un request por parte un usuario.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
    """
    return render(request, 'rol/rol_opciones_sistema.html')


# === listar roles ===
class ListaRol_sistema(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion de todas las intancias del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
    """
    paginate_by = 3
    model = Group
    template_name = 'rol/rol_lista_sistema.html'
    permission_required = 'usuario.listar_rol_sistema'

    # La lista a mostrar estara por orden ascendente
    # class Meta:
    # ordering = ['-id']
    def get_queryset(self):
        return Group.objects.order_by('id').distinct()


@permission_required('usuario.listar_rol_sistema', raise_exception=True)
def search_sistema(request):
    """
    Permite la búsqueda de las intancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Lista todas las instancias del modelo Group que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'rol/list_busqueda_sistema.html'
    query = request.GET.get('buscar')

    if query:
        results = Group.objects.filter(Q(name__icontains=query)).order_by('id').distinct()
    else:
        results = Group.objects.all().order_by('id')

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template, {'page_obj': page_obj})


# === editar rol ===
class EditarRol_sistema(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de una instancia del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Se modifica la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
    """
    model = Group
    form_class = GroupForm_sistema
    permission_required = 'usuario.editar_rol_sistema'
    template_name = 'rol/rol_editar_sistema.html'
    success_url = reverse_lazy('rol:rol_lista_sistema')


# === eliminar rol ===
class EliminarRol_sistema(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Se elimina la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
    """
    model = Group
    template_name = 'rol/rol_eliminar_sistema.html'
    permission_required = 'usuario.eliminar_rol_sistema'
    success_url = reverse_lazy('rol:rol_lista_sistema')

# === FIN ====

# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
