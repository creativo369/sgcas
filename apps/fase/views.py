from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from guardian.mixins import PermissionRequiredMixin
from apps.fase.forms import FaseForm, FaseUpdateForm, FaseCambiarEstadoForm
from apps.fase.models import Fase
from django.views.generic import CreateView

from apps.proyecto.models import Proyecto


class FaseCrear(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Crea una instancia de fase<br/>
    **:param PermissionRequiredMixin:** Libreria que gestiona el permiso para la creación de fases.<br/>
    **:param LoginRequiredMixin:** Requiere estar logueado, de la libreria django.contrib.auth.mixins<br/>
    **:param CreateView:** Recibe una vista generica de tipo CreateView para vistas basadas en clases.<br/>
    **:return:** Retorna una instancia del modelo Fase
    """
    model = Fase
    permission_required = 'fase.crear_fase'
    template_name = 'fase/fase_crear.html'
    success_url = 'fase:fase_lista'

    def get(self, request, *args, **kwargs):
        form = FaseForm(_id=kwargs.get('_id'))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        id_proyecto = kwargs.pop('_id')
        form = FaseForm(request.POST, _id=id_proyecto)
        if form.is_valid():
            fase = form.save(commit=False)
            fase.proyecto = Proyecto.objects.get(id=id_proyecto)
            fase.save()
            form.save_m2m()
        return redirect(self.success_url, _id=id_proyecto)


@login_required
@permission_required('fase.ver_fase')
def fase_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo Fase.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema<br/>
    """

    return render(request, 'fase/fase_opciones.html')

@permission_required('fase.detalles_fase')
def fase_detalles(request, pk):
    """
    Permite visualizar los detalles una fase de un proyecto.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe un pk correspondiente a la fase que se desea visualizar.<br/>
    **:return:** Retorna una plantilla que despliega los detalles de una fase.<br/>
    """
    return render(request, 'fase/fase_detalles.html', {'fase': Fase.objects.get(id=pk)})

@permission_required('fase.listar_fase')
def lista_fase(request, _id):
    """
    Permite visualizar todas las fases de un proyecto.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param _id:** Recibe un pk del proyecto del cual se desea obtener las fases.<br/>
    **:return:** Retorna una plantilla que despliega todas las fases de un proyecto.<br/>
    """
    proyecto = Proyecto.objects.get(id=_id)
    fase = Fase.objects.filter(proyecto=proyecto)  # Queryset
    context = {
        'fases_proyecto': fase,
        'proyecto': proyecto
    }
    return render(request, 'fase/fase_lista.html', context)

@permission_required('fase.cambio_estado_fase')
def cambiar_estado_fase(request, pk, _id):
    """
    Permite la modificacion del estado de una fase.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:**Recibe el pk de la fase de la cual se desea cambiar el estado<br/>
    **:param _id:** Recibe un pk del proyecto al cual pertenece la fase para luego redirigirse a la lista de fases.<br/>
    **:return:** Retorna la fase de un estado cambiada o no, luego se redirige a la lista de fases del proyecto.<br/>
    """
    fase = get_object_or_404(Fase, pk=pk)
    form = FaseCambiarEstadoForm(request.POST or None, instance=fase)
    if form.is_valid():
        form.save()
        return redirect('fase:fase_lista', _id=_id)
    return render(request, 'fase/fase_cambiar_estado.html', {'form': form})

@permission_required('fase.eliminar_fase')
def eliminar_fase(request, pk, _id):
    """
    Permite la eliminacion de una instancia de objecto fase.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:**Recibe el pk de la fase que se desea eliminar<br/>
    **:param _id:** Recibe un pk del proyecto al cual pertenece la fase para luego redirigirse a la lista de fases.<br/>
    **:return:** Se elimina la instancia para luego redirigirse  la lista de fases del proyecto.<br/>
        """
    success_url = 'fase:fase_lista'
    fase = Fase.objects.get(id=pk)
    fase.delete()
    return redirect(success_url, _id=_id)

@permission_required('fase.editar_fase')
def fase_modificar(request, pk, _id):
    """
    Permite la modificacion de una instancia de objecto fase.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:**Recibe el pk de la fase que se desea modificar<br/>
    **:param _id:** Recibe un pk del proyecto al cual pertenece la fase para luego redirigirse a la lista de fases.<br/>
    **:return:** Se modifica la instancia de fase para luego redirigirse a la lista de fases del proyecto.<br/>
    """
    fase = get_object_or_404(Fase, id=pk)
    form = FaseUpdateForm(request.POST or None, instance=fase)
    if form.is_valid():
        form.save()
        return redirect('fase:fase_lista', _id=_id)
    return render(request, 'fase/fase_crear.html', {'form': form})

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
