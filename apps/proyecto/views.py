from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from guardian.mixins import PermissionRequiredMixin

from .models import Proyecto
from .forms import ProjectoForm


###################### Vistas basadas en Funciones #####################################

def home(request):
    """
        Recibe una petición a la URL por parte de un cliente, esta función retorna
        la pagina principal de la definición de proyecto
        Args 	: request.
        Return 	: retorno el layout de la definición de proyetos proyecto_home.html
    """
    return render(request, 'proyecto/home.html')


def success(request):
    return render(request, 'proyecto/success.html')


###################### Vistas basadas en Clases ########################################

class CrearProyecto(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion de todas las instancias de modelo Proyecto.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param CreateView: Recibe una vista generica de tipo CreateView para vistas basadas en clases.
    :return: Crea una intancia de modelo proyecto.
    """
    model = Proyecto
    form_class = ProjectoForm
    permission_required = 'proyecto.add_proyecto'
    template_name = 'proyecto/crear_proyecto.html'
    success_url = reverse_lazy('proyecto:success')

    # login_url = 'client_login'  Se necesita vincular

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  # intuimos quien es el creador del proyecto = gerente
        self.object.save()  # (el que esta logeado y crea el proyecto)
        form.save_m2m()  # Para guardar as relaciones many to many
        return HttpResponseRedirect(self.get_success_url())


class ListaProyecto(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion de todas las instancias de modelo Proyecto.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: Una vista de todas las intancias a traves del archivo listado_proyecto.html.
    """
    # login_url = 'client_login'  Se necesita vincular
    model = Proyecto
    permission_required = 'proyecto.view_proyecto'
    template_name = 'proyecto/listado_proyecto.html'


class ActualizarProyecto(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """
    Permite la actualizacion una instancia de modelo Proyecto.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return: Actualiza una instancia del modelo Proyecto, luego se redirige a la lista de proyectos.
    """
    model = Proyecto
    template_name = 'proyecto/edit.html'
    form_class = ProjectoForm
    permission_required = 'proyecto.change_proyecto'
    success_url = reverse_lazy('proyecto:listado_proyecto')


class EliminarProyecto(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """
    Permite la eliminacion una instancia de modelo Proyecto.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param LoginRequiredMixin: Requiere estar logueado, de la libreria django.contrib.auth.mixins
    :param DeleteView: Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return: Eliminar una instancia del modelo Proyecto, luego se redirige a la lista de proyectos.
    """
    model = Proyecto
    template_name = 'proyecto/delete.html'
    permission_required = 'proyecto.delete_proyecto'
    success_url = reverse_lazy('proyecto:listado_proyecto')
