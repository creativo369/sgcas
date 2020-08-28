# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rol.forms import GroupForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from apps.rol.models import Rol
from apps.fase.models import Fase

"""
Todas las vistas para la aplicación del Modulo Rol
Actualmente se despliega en las plantillas 6 vistas:

1. **crear_rol_view** - funcion para la creación de roles  (Ir a la sección: [[views.py #crear rol]] )
2. **rol_opciones** - despliega opciones  (Ir a la sección: [[views.py #rol opciones]] )
3. **ListaRol** - Lista los roles existentes (Ir a la sección: [[views.py #listar roles]] )
4. **search** - lista los roles buscados (Ir a la sección: [[views.py #search]] )
5. **EditarRol** - modifica los atributos de un rol (Ir a la sección: [[views.py #editar rol]] )
6. **EliminarRol** - elimina un rol (Ir a la sección: [[views.py #eliminar rol]] )
"""

#Vista que redefine la vista predeterminada del error 403.
def handler403(request, exception, template_name='403.html'):
    response = render(request,'rol/403.html')
    response.status_code = 403
    return response

@login_required
@permission_required('usuario.crear_rol', raise_exception=True)
# === crear rol ===
def crear_rol_view(request, id_fase):
    """
    Permite la visualizacion de la plantilla para la creacion de instancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Se almacena una instancia del modelo Group.<br/>
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


# @login_required
# @permission_required('usuario.ver_rol', raise_exception=True)
# # === rol opciones ===
# def rol_opciones(request):
#     """
#     Permite la visualizacion de las opciones sobre el modelo Group.<br/>
#     **:param request:** Recibe un request por parte un usuario.<br/>
#     **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
#     """
#     return render(request, 'rol/rol_opciones.html')

# === listar roles ===
def lista_rol(request, id_fase):
    return render(request, 'rol/rol_lista.html', {'object_list':Rol.objects.filter(fase=get_object_or_404(Fase, pk=id_fase))})

# class ListaRol(PermissionRequiredMixin, ListView):
#     """
#     Permite la visualizacion de todas las intancias del modelo Group.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
#     **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
#     **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
#     """
#     paginate_by = 3
#     model = Group
#     template_name = 'rol/rol_lista.html'
#     permission_required = 'usuario.listar_rol'

#     # La lista a mostrar estara por orden ascendente
#     #class Meta:
#         #ordering = ['-id']
#     def get_queryset(self):
#         return Group.objects.order_by('id').distinct()

@permission_required('usuario.listar_rol', raise_exception=True) 
def search(request):
    """
    Permite la búsqueda de las intancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>    
    **:return:** Lista todas las instancias del modelo Group que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'rol/list_busqueda.html'
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
def editar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    group = rol.group
    form = GroupForm(request.POST or None, instance = group)
    if form.is_valid():
        group = form.save()
        rol.group = group
        return redirect('rol:rol_lista', id_fase=id_fase)
    return render(request,'rol/rol_crear.html', {'form':form}) 

# === Eliminar rol
def eliminar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    id_fase = rol.fase.pk
    rol.delete()
    return redirect('rol:rol_lista', id_fase=id_fase)



# class EditarRol(PermissionRequiredMixin, UpdateView):
#     """
#     Permite la modificacion de una instancia del modelo Group.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
#     **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
#     **:return:** Se modifica la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
#     """
#     model = Group
#     form_class = GroupForm
#     permission_required = 'usuario.editar_rol'
#     template_name = 'rol/rol_editar.html'
#     success_url = reverse_lazy('rol:rol_lista')

# === eliminar rol ===
# class EliminarRol(PermissionRequiredMixin, DeleteView):
#     """
#     Permite la eliminacion de una instancia del modelo Group.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
#     **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
#     **:return:** Se elimina la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
#     """
#     model = Group
#     template_name = 'rol/rol_eliminar.html'
#     permission_required = 'usuario.eliminar_rol'
#     success_url = reverse_lazy('rol:rol_lista')

# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)