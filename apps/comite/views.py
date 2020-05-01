from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Comite
from .forms import FormularioComite, FormularioComiteUpdate
from ..proyecto.models import Proyecto


@login_required
def success(request):
    """
    Una vista basada en función donde indica la creación exitosa de una operacion sobre proyectos.
    :param request: recibe la petición del cliente.
    :return: plantilla mostrando la operación exitosa.
    """
    return render(request, 'comite/success.html')


class CreateComite(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion en una plantilla para la definición de un proyecto.
    :param PermissionRequiredMixin: Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de crear proyectos.
    :param LoginRequiredMixin: Requiere que el usuario este logueado en el sistema.
    :param CreateView: Recibe una vista generica de tipo CreateView para vistas basadas en clases.
    :return: Crea una instancia del modelo proyecto y lo guarda en la base de datos.
    """
    model = Comite
    permission_required = 'comite.add_comite'
    template_name = 'comite/create.html'
    template_detail = 'comite/detail.html'
    success_url = 'proyecto:detail'


    def get(self, request, *args, **kwargs):
        """
        Obtiene el formulario de creación de un comité
        :param request: recibe la petición del cliente que solicita crear un comite para la instancia del proyecto
        :param args:
        :param kwargs: Diccionario 'clave':valor que recibe la referencia de la instancia del modelo proyecto
        :return: el formulario , la plantilla donde se va desplegar el formulario de creación
        """
        comite_query = Comite.objects.filter(proyecto=Proyecto.objects.get(id=kwargs.get('_id')))
        if not comite_query.exists():
            form = FormularioComite(_id=kwargs.pop('_id'))
            return render(request, self.template_name, {'formulario': form})
        else:
            return render(request, self.template_detail, {'comite': comite_query.first()})

    def post(self, request, *args, **kwargs):
        """
        Almacena los datos obtenidos del formulario en la base de datos
        :param request:
        :param args:
        :param kwargs: Diccionario 'clave':valor que recibe la referencia de la instancia del modelo proyecto
        :return: Redirige a la plantilla de Operación exitosa de la creación de un comité
        """
        id_proyecto = kwargs.pop('_id')  # Guardamos en una variable el id del proyecto
        form = FormularioComite(request.POST, _id=id_proyecto)
        if form.is_valid():
            comite = form.save(commit=False)
            comite.proyecto = Proyecto.objects.get(id=id_proyecto)  # Establece el foreign key con proyecto
            comite.save()
            form.save_m2m()
        return redirect(self.success_url, pk=id_proyecto)


class UpdateComite(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
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
    form_class = FormularioComiteUpdate
    permission_required = 'comite.change_comite'
    success_url = reverse_lazy('proyecto:list')

    def form_valid(self, form):
        comite = form.save()
        return redirect(self.success_url)


class DeleteComite(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
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
    success_url = reverse_lazy('proyecto:list')


class DetailComite(LoginRequiredMixin, DetailView, PermissionRequiredMixin):
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
