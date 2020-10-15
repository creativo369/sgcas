from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from guardian.mixins import PermissionRequiredMixin

from SGCAS.decorators import requiere_permiso
from apps.fase.forms import FaseForm, FaseUpdateForm, FaseCambiarEstadoForm
from apps.fase.models import Fase
from django.db.models import Q
from django.views.generic import CreateView
from apps.proyecto.models import Proyecto

"""
Todas las vistas para la aplicación del Modulo Fase
Actualmente se despliega en las plantillas 7 vistas:

1. **FaseCrear** - se ocupa de la creación de la fase (Ir a la sección: [[views.py #crear fase]] )
2. **fase_detalles** - permite visualizar información relevante de una fase (Ir a la sección: [[views.py #fase detalles]] )
3. **lista_fase** - lista las fases de un proyecto (Ir a la sección: [[views.py #lista fase]] )
4. **search** - despliga una lista de fases buscadas dentro de un proyecto (Ir a la sección: [[views.py #search]] )
5. **cambiar_estado_fase** - cambia de estado una fase a abierta o cerrada (Ir a la sección: [[views.py #cambia estado fase]] )
6. **eliminar_fase** - elimina una fase de la base de datos (Ir a la sección: [[views.py #eliminar fase]] )
7. **fase_modificar** - permite efectuar modificaciones a una determinada fase (Ir a la sección: [[views.py #fase modificar]] )
"""


# === crear fase ===
class FaseCrear(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Crea una instancia de fase<br/>
    **:param PermissionRequiredMixin:** Libreria que gestiona el permiso para la creación de fases.<br/>
    **:param LoginRequiredMixin:** Requiere estar logueado, de la libreria django.contrib.auth.mixins<br/>
    **:param CreateView:** Recibe una vista generica de tipo CreateView para vistas basadas en clases.<br/>
    **:return:** Retorna una instancia del modelo Fase.<br/>
    """
    model = Fase
    permission_required = 'fase.crear_fase'
    template_name = 'fase/fase_crear.html'
    success_url = 'fase:fase_lista'

    def get(self, request, *args, **kwargs):
        """

        Se obtiene la instacia del modelo proyecto en el cual se desea crear la fase.<br/>
        **:param request:** recibe la petición del cliente de crear una instancia de fase dentro del proyecto.<br/>
        :param args:<br/>
        **:param kwargs:** Diccionario 'clave':valor que recibe la referencia del proyecto al que estará asociada la fase.<br/>
        **:return:** redirige a la plantilla de creación de la fase.<br/>

        """
        proyecto = Proyecto.objects.get(pk=kwargs.get('_id'))
        if proyecto.estado != 'Iniciado':
            form = FaseForm(_id=kwargs.get('_id'))
            return render(request, self.template_name, {'form': form, 'proyecto': proyecto})
        return render(request, self.template_name, {'proyecto': proyecto})

    def post(self, request, *args, **kwargs):
        """

        Se almacena en la base de datos la intancia de la fase recien creada.<br/>
        **:param request:** recibe la petición del cliente para guardar la fase recién creada.<br/>
        :param args:<br/>
        **:param kwargs:** Diccionario 'clave':valor que recibe la referencia del proyecto al que estará asociada la fase.<br/>
        **:return:** redirige a la plantilla que contiene la lista de fases del proyecto.<br/>

        """
        id_proyecto = kwargs.pop('_id')
        form = FaseForm(request.POST, _id=id_proyecto)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
            if Fase.objects.filter(Q(nombre=nombre) & Q(proyecto=proyecto)).exists():
                return render(request, 'fase/validate_fase.html')
            fase = form.save(commit=False)
            fase.proyecto = Proyecto.objects.get(id=id_proyecto)
            fase.save()
            form.save_m2m()
        return redirect(self.success_url, _id=id_proyecto)


@login_required
@permission_required('fase.gestion_fase', raise_exception=True)
# === fase opciones ===
def fase_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo Fase.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema.<br/>
    """

    return render(request, 'fase/fase_opciones.html')


# === fase detalles ===
# @requiere_permiso('detalles_fase')
@permission_required('fase.detalles_fase', raise_exception=True)
def fase_detalles(request, id_fase):
    """
    Permite visualizar los detalles una fase de un proyecto.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe un pk correspondiente a la fase que se desea visualizar.<br/>
    **:return:** Retorna una plantilla que despliega los detalles de una fase.<br/>
    """
    context = {
        'fase': Fase.objects.get(id=id_fase),
        'proyecto': Fase.objects.get(id=id_fase).proyecto
    }
    return render(request, 'fase/fase_detalles.html', context)


@permission_required('fase.listar_fase', raise_exception=True)
# @requiere_permiso('listar_fase')
# === lista fase ===
def lista_fase(request, _id):
    """
    Permite visualizar todas las fases de un proyecto.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param _id:** Recibe un pk del proyecto del cual se desea obtener las fases.<br/>
    **:return:** Retorna una plantilla que despliega todas las fases de un proyecto.<br/>
    """
    proyecto = Proyecto.objects.get(id=_id)
    fase = Fase.objects.filter(proyecto=proyecto).order_by('id').distinct()  # Queryset

    paginator = Paginator(fase, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'fases_proyecto': fase,
        'proyecto': proyecto,
        'page_obj': page_obj
    }
    return render(request, 'fase/fase_lista.html', context)


@permission_required('fase.listar_fase', raise_exception=True)
# @requiere_permiso('listar_fase')
# === search ===
def search(request, _id):
    """
    Permite realizar la búsqueda de fases en dentro de un determinado proyecto.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param _id:** Recibe un pk del proyecto del cual se desea obtener las fases.<br/>
    **:return:** Retorna una plantilla con las fases que cumplan con los parametros de búsqueda recibidos.<br/>
    """
    template = 'fase/list_busqueda.html'
    query = request.GET.get('buscar')
    proyecto = Proyecto.objects.get(id=_id)

    if query:
        results = Fase.objects.filter(
            Q(proyecto=proyecto) & (Q(nombre__icontains=query) | Q(descripcion__contains=query))).order_by(
            'id').distinct()
    else:
        results = Fase.objects.filter(Q(proyecto=proyecto)).order_by('id').distinct()

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'fases_proyecto': results,
        'proyecto': proyecto,
        'page_obj': page_obj
    }
    return render(request, template, context)


@permission_required('fase.cambio_estado_fase', raise_exception=True)
# @requiere_permiso('cambio_estado_fase')
# === cambia estado fase ===
def cambiar_estado_fase(request, id_fase, _id):
    """
    Permite la modificación del estado de una fase.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:**Recibe el pk de la fase de la cual se desea cambiar el estado.<br/>
    **:param _id:** Recibe un pk del proyecto al cual pertenece la fase para luego redirigirse a la lista de fases.<br/>
    **:return:** Retorna la fase de un estado cambiada o no, luego se redirige a la lista de fases del proyecto.<br/>
    """
    fase = get_object_or_404(Fase, id=id_fase)
    form = FaseCambiarEstadoForm(request.POST or None, instance=fase)
    if form.is_valid():
        form.save()
        return redirect('fase:fase_lista', _id=_id)
    elif fase.proyecto.estado == "Iniciado":
        return render(request, 'fase/fase_cambiar_estado.html',
                      {'form': form, 'fase': fase, 'proyecto': Fase.objects.get(id=id_fase).proyecto})
    else:
        return render(request, 'fase/fase_cambiar_estado.html', {'fase': fase})


@permission_required('fase.eliminar_fase', raise_exception=True)
# @requiere_permiso('eliminar_fase')
# === eliminar fase ===
def eliminar_fase(request, id_fase, _id):
    """
    Permite la eliminación de una instancia de objecto fase.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:**Recibe el pk de la fase que se desea eliminar<br/>
    **:param _id:** Recibe un pk del proyecto al cual pertenece la fase para luego redirigirse a la lista de fases.<br/>
    **:return:** Se elimina la instancia para luego redirigirse  la lista de fases del proyecto.<br/>
        """
    success_url = 'fase:fase_lista'
    fase = Fase.objects.get(id=id_fase)
    if fase.proyecto.estado == "Iniciado":
        return render(request, 'fase/fase_eliminar.html', {'fase': fase})
    else:
        fase.delete()
    return redirect(success_url, _id=_id)


@permission_required('fase.editar_fase', raise_exception=True)
# @requiere_permiso('editar_fase')
# === fase modificar ===
def fase_modificar(request, id_fase, _id, *args, **kwargs):
    """
    Permite la modificación de una instancia de objecto fase.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:**Recibe el pk de la fase que se desea modificar.<br/>
    **:param _id:** Recibe un pk del proyecto al cual pertenece la fase para luego redirigirse a la lista de fases.<br/>
    **:return:** Se modifica la instancia de fase para luego redirigirse a la lista de fases del proyecto.<br/>
    """
    fase = get_object_or_404(Fase, id=id_fase)
    miembros_proyecto_queryset = fase.proyecto.miembros.all()
    form = FaseUpdateForm(request.POST or None, instance=fase, miembros=miembros_proyecto_queryset)
    if form.is_valid():
        form.save()
        return redirect('fase:fase_lista', _id=_id)
    return render(request, 'fase/fase_modificar.html', {'form': form})

# **Volver atras** : [[forms.py]]

# **Ir a la documentación de pruebas unitarias del modulo fase** : [[tests.py]]

# === Indice de la documentación de la Aplicación fase  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
