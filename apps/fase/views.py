from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from guardian.mixins import PermissionRequiredMixin
from apps.fase.forms import FaseForm, FaseUpdateForm, FaseCambiarEstadoForm
from apps.fase.models import Fase
from django.views.generic import CreateView

from apps.proyecto.models import Proyecto


class FaseCrear(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Fase
    permission_required = 'fase.add_fase'
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
# @permission_required('fase.view_fase')
def fase_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo Fase.
    :param request:Recibe un request por parte de un usuario.
    :return: Renderiza la plantilla usuario_home.html que es el home del sistema
    """

    return render(request, 'fase/fase_opciones.html')


def fase_detalles(request, pk):
    return render(request, 'fase/fase_detalles.html', {'fase': Fase.objects.get(id=pk)})


def lista_fase(request, _id):
    proyecto = Proyecto.objects.get(id=_id)
    fase = Fase.objects.filter(proyecto=proyecto)  # Queryset
    context = {
        'fases_proyecto': fase,
        'proyecto': proyecto
    }
    return render(request, 'fase/fase_lista.html', context)


def cambiar_estado_fase(request, pk, _id):
    fase = get_object_or_404(Fase, pk=pk)
    form = FaseCambiarEstadoForm(request.POST or None, instance=fase)
    if form.is_valid():
        form.save()
        return redirect('fase:fase_lista', _id=_id)
    return render(request, 'fase/fase_cambiar_estado.html', {'form': form})


def eliminar_fase(request, pk, _id):
    success_url = 'fase:fase_lista'
    fase = Fase.objects.get(id=pk)
    fase.delete()
    return redirect(success_url, _id=_id)


def fase_modificar(request, pk, _id):
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
