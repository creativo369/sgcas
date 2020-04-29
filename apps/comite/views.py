from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Comite
from .forms import FormularioComite
from SGCAS.decorators import administrator_only
from ..proyecto.models import Proyecto


@login_required
def manage_comite(request):
    """
    Recibe una petición a la pagina de proyecto por parte de un cliente, esta vista basada en una función retorna
    la pagina principal para la gestión de proyectos.

    :param : request
    :return: retorna la plantilla de gestión de proyectos
    """
    return render(request, 'comite/manage_comite.html')


@login_required
def success(request):
    """
    Una vista basada en función donde indica la creación exitosa de una operacion sobre proyectos.
    :param request: recibe la petición del cliente.
    :return: plantilla mostrando la operación exitosa.
    """
    return render(request, 'comite/success.html')


class create(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion en una plantilla para la definición de un proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de crear proyectos.
    :param LoginRequiredMixin: Requiere que el usuario este logueado en el sistema.
    :param CreateView: Recibe una vista generica de tipo CreateView para vistas basadas en clases.
    :return: Crea una instancia del modelo proyecto y lo guarda en la base de datos.
    """
    model = Comite
    # form_class = FormularioComite
    permission_required = 'comite.add_comite'
    template_name = 'comite/create.html'
    success_url = reverse_lazy('comite:success')

    def get(self, request, *args, **kwargs):
        form = FormularioComite(_id=kwargs.pop('_id'))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        id_proyecto = kwargs.pop('_id') #Gurdamos en una variable el id del proyecto
        form = FormularioComite(request.POST, _id=id_proyecto)
        if form.is_valid():
            comite = form.save(commit=False)
            comite.proyecto = Proyecto.objects.get(id=id_proyecto)  # Establece el foreign key con proyecto
            comite.save()
            form.save_m2m()
        return redirect(self.success_url)


class list(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion de los proyectos.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de visualizar proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: Una vista de todos los proyectos.
    """
    model = Comite
    permission_required = 'comite.view_comite'
    template_name = 'comite/list.html'


class update(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """
    Permite la actualizacion una instancia de modelo Proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de modificación de proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return: Actualiza una instancia del modelo Proyecto, luego se redirige a la lista de proyectos.
    """
    model = Comite
    template_name = 'comite/update.html'
    form_class = FormularioComite
    permission_required = 'comite.change_comite'

    # success_url = reverse_lazy('comite:detail')
    def form_valid(self, form):
        object = form.save()
        return redirect('comite:detail', pk=object.pk)


class delete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """
    Permite suprimir una instancia del modelo de Proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de eliminar proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param DeleteView: Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return: Eliminar una instancia del modelo Proyecto, luego se redirige a la lista de proyectos.
    """
    model = Comite
    template_name = 'comite/delete.html'
    permission_required = 'comite.delete_comite'
    success_url = reverse_lazy('comite:list')


class detail(LoginRequiredMixin, DetailView, PermissionRequiredMixin):
    """
    Despliega los detalles de una instancia del modelo de Proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de eliminar proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param DetailView: Recibe una vista generica de tipo DetailView para vistas basadas en clases.
    :return: Despliega los detalles de una instancia del modelo Proyecto.
    """
    model = Comite
    template_name = 'comite/detail.html'
    permission_required = 'comite.view_comite'
    success_url = reverse_lazy('comite:list')
