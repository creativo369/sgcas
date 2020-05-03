from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from guardian.decorators import permission_required
from guardian.mixins import PermissionRequiredMixin
from apps.fase.forms import FaseForm, FaseUpdateForm, FaseCambiarEstadoForm
from apps.fase.models import Fase
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy, reverse

from apps.proyecto.models import Proyecto


# @login_required
# # @permission_required('fase.add_fase')
# def crear_fase(request, _id):
#     """
#     Permite la creacion de instancias de modelo Fase.
#     :param request: Recibe un request por parte de un usuario.
#     :return:  Retorna una instancia del modelo Fase.
#     """
#     if request.method == 'POST':
#         form = FaseForm(request.POST, _id=_id)
#         if form.is_valid():
#             fase = form.save(commit=False)
#             fase.proyecto = Proyecto.objects.get(id=_id)
#             fase.save()
#             form.save_m2m()
#         return redirect('fase:fase_opciones')
#     else:
#         form = FaseForm(_id=_id)
#     return render(request, 'fase/fase_crear.html', {'form': form})


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

# # class FaseLista(PermissionRequiredMixin, ListView):
# class FaseLista(ListView):
#     """
#     Permite la visualizacion en lista de todas las intancias del modelo Fase
#     :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
#     :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
#     :return: Una vista de todas las intancias a traves del archivo fase_lista.html.
#     """
#     model = Fase
#     template_name = 'fase/fase_lista.html'
#
#     # permission_required = 'fase.view_fase'
#
#     # La lista a mostrar estara por orden ascendente
#     class Meta:
#         ordering = ['-id']


# # class FaseEliminar(PermissionRequiredMixin, DeleteView):
# class FaseEliminar(DeleteView):
#     """
#     Permite la eliminacion instancias de modelos Fase.
#     :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
#     :param DeleteView: Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
#     :return: Elimina una instancia del modelo Fase del sistema.
#     """
#     model = Fase
#     template_name = 'fase/fase_eliminar.html'
#     # permission_required = 'fase.delete_fase'
#     success_url = reverse_lazy('fase:fase_lista')


# # class FaseModificar(PermissionRequiredMixin, UpdateView):
# class FaseModificar(UpdateView):
#     """
#     Permite la modificacion de informacion de una instancia de modelo Fase.
#     :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
#     :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
#     :return: Modficia na instancia del modelo Fase, luego se redirige a la lista de fases.
#     """
#     model = Fase
#     template_name = 'fase/fase_modificar.html'
#     form_class = FaseUpdateForm
#     # permission_required = 'fase.change_fase'
#     success_url = reverse_lazy('fase:fase_lista')
