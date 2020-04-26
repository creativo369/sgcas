from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Proyecto
from .forms import FormularioProyecto, FormularioProyectoUpdate
from SGCAS.decorators import administrator_only


@login_required
def manage_projects(request):
    """
    Recibe una petición a la pagina de proyecto por parte de un cliente, esta vista basada en una función retorna
    la pagina principal para la gestión de proyectos.

    :param : request
    :return: retorna la plantilla de gestión de proyectos
    """
    return render(request, 'proyecto/manage_projects.html')


@login_required
def success(request):
    """
    Una vista basada en función donde indica la creación exitosa de una operacion sobre proyectos.
    :param request: recibe la petición del cliente.
    :return: plantilla mostrando la operación exitosa.
    """
    return render(request, 'proyecto/success.html')


class create(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion en una plantilla para la definición de un proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de crear proyectos.
    :param LoginRequiredMixin: Requiere que el usuario este logueado en el sistema.
    :param CreateView: Recibe una vista generica de tipo CreateView para vistas basadas en clases.
    :return: Crea una instancia del modelo proyecto y lo guarda en la base de datos.
    """
    model = Proyecto
    form_class = FormularioProyecto
    permission_required = 'proyecto.add_proyecto'
    template_name = 'proyecto/create.html'
    success_url = reverse_lazy('proyecto:success')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  # intuimos que el creador del proyecto va ser el gerente
        self.object.save()
        form.save_m2m()  # Para guardar as relaciones manytomany
        return HttpResponseRedirect(self.get_success_url())


class list(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion de los proyectos.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de visualizar proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: Una vista de todos los proyectos.
    """
    model = Proyecto
    permission_required = 'proyecto.view_proyecto'
    template_name = 'proyecto/list.html'


class update(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """
    Permite la actualizacion una instancia de modelo Proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de modificación de proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return: Actualiza una instancia del modelo Proyecto, luego se redirige a la lista de proyectos.
    """
    model = Proyecto
    template_name = 'proyecto/update.html'
    form_class = FormularioProyectoUpdate
    permission_required = 'proyecto.change_proyecto'

    # success_url = reverse_lazy('proyecto:detail')
    def form_valid(self, form):
        object = form.save()
        return redirect('proyecto:detail', pk=object.pk)


class delete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """
    Permite suprimir una instancia del modelo de Proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de eliminar proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param DeleteView: Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return: Eliminar una instancia del modelo Proyecto, luego se redirige a la lista de proyectos.
    """
    model = Proyecto
    template_name = 'proyecto/delete.html'
    permission_required = 'proyecto.delete_proyecto'
    success_url = reverse_lazy('proyecto:list')


class detail(LoginRequiredMixin, DetailView, PermissionRequiredMixin):
    """
    Despliega los detalles de una instancia del modelo de Proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de eliminar proyectos.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param DetailView: Recibe una vista generica de tipo DetailView para vistas basadas en clases.
    :return: Despliega los detalles de una instancia del modelo Proyecto.
    """
    model = Proyecto
    template_name = 'proyecto/detail.html'
    permission_required = 'proyecto.view_proyecto'
    success_url = reverse_lazy('proyecto:list')
