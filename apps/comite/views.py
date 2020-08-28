# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

# === Importación de los codigos fuentes de la aplicación ===
from .models import Comite
from .forms import FormularioComite, FormularioComiteUpdate
from ..proyecto.models import Proyecto

"""
Todas las vistas para la aplicación del Modulo Comité
Actualmente se despliega en las plantillas 5 vistas:




1. **success** - operación exitosa para la creación de un comite (Ir a la sección: [[views.py #success]] )
2. **CreateComite** - definición de una instancia del modelo comité (Ir a la sección: [[views.py #create comite]] )
3. **UpdateComite** - modificar una instancia del modelo comité (Ir a la sección: [[views.py #update comite]] )
4. **DeleteComite** - suprimir una instancia del modelo comité (Ir a la sección: [[views.py #delete comite]] )
5. **DetailComite** - ver detalles de una instancia del modelo comité (Ir a la sección: [[views.py #detail comite]] )


"""


# === success ===
@login_required
def success(request):
    """
    Una vista basada en función donde indica la creación exitosa de una operacion sobre comites.<br/>
    **:param request:** recibe la petición del cliente.<br/>
    **:return:** plantilla mostrando la operación exitosa.<br/>
    """
    return render(request, 'comite/success.html')


# === create comite ===
class CreateComite(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la visualizacion en una plantilla para la definición de un comite.<br/>
    **:param PermissionRequiredMixin:** Libreria que gestiona el permiso para la creación de comites.El usuario
    debe poseer el permiso correspondiente de crear comite.<br/>
    **:param LoginRequiredMixin:** Requiere que el usuario este logueado en el sistema.<br/>
    **:param CreateView:** Recibe una vista generica de tipo CreateView para vistas basadas en clases.<br/>
    **:return:** Crea una instancia del modelo comite y lo guarda en la base de datos.<br/>
    """
    model = Comite
    permission_required = 'comite.crear_comite'
    template_name = 'comite/create.html'
    template_detail = 'comite/detail.html'
    template_alert = 'comite/alert.html'
    success_url = 'proyecto:detail'

    def get(self, request, *args, **kwargs):
        """

        Obtiene el formulario de creación de un comité para validar que un proyecto tenga previamente un comité.<br/>
        **:param request:** recibe la petición del cliente que solicita crear un comite para la instancia del proyecto.<br/>
        :param args:<br/>
        **:param kwargs:** Diccionario 'clave':valor que recibe la referencia de la instancia del modelo proyecto.<br/>
        **:return:** el formulario , la plantilla donde se va desplegar el formulario de creación.<br/>

        """
        comite_query = Comite.objects.filter(proyecto=Proyecto.objects.get(id=kwargs.get('_id')))
        proyecto_query = Proyecto.objects.get(id=kwargs.get('_id'))
        # num_user_proyect = Proyecto.objects.get(id=kwargs.get('_id')).miembros
        cantidad_miembros = len(Proyecto.objects.get(id=kwargs.get('_id')).miembros.all())

        if cantidad_miembros >= 3:
            if not comite_query.exists():
                form = FormularioComite(_id=kwargs.pop('_id'))
                instancia_proyecto = proyecto_query
                return render(request, self.template_name, {'formulario': form, 'proyecto': instancia_proyecto})
            else:
                return render(request, self.template_detail, {'comite': comite_query.first()})
        else:
            # Redirigir a template de 3 usuarios como minimo en el proyecto para
            # crear comite
            return render(request, self.template_alert)

    def post(self, request, *args, **kwargs):
        """

        Almacena los datos obtenidos del formulario en la base de datos.<br/>
        **:param request:** La petición del cliente.<br/>
        **:param args:**<br/>
        **:param kwargs:** Diccionario 'clave':valor que recibe la referencia de la instancia del modelo comite.<br/>
        **:return:** Redirige a la plantilla de Operación exitosa de la creación de un comité.<br/>

        """
        id_proyecto = kwargs.pop('_id')  # Guardamos en una variable el id del proyecto
        form = FormularioComite(request.POST, _id=id_proyecto)
        if form.is_valid():
            comite = form.save(commit=False)
            comite.proyecto = Proyecto.objects.get(id=id_proyecto)  # Establece el foreign key con proyecto

            comite.save()
            form.save_m2m()
        return redirect(self.success_url, pk=id_proyecto)


# === update comite ===
class UpdateComite(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """
    Permite la actualizacion una instancia de modelo comite.<br/>
    **:param PermissionRequiredMixin:** Libreria que gestiona el permiso para la creación de comites.El usuario
    debe poseer el permiso correspondiente de modificación de comites.<br/>
    **:param LoginRequiredMixin:** Requiere estar logueado, de la libreria django.contrib.auth.mixins<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Actualiza una instancia del modelo comite, luego se redirige a la lista de proyectos.<br/>
    """
    model = Comite
    template_name = 'comite/update.html'
    form_class = FormularioComiteUpdate
    permission_required = 'comite.editar_comite'
    success_url = reverse_lazy('proyecto:list')

    def get(self, request, *args, **kwargs):
        """
        Obtiene el formulario de creación de un comité para validar que un proyecto tenga previamente un comité.<br/>
        **:param request:** recibe la petición del cliente que solicita crear un comite para la instancia del proyecto.<br/>
        :param args:<br/>
        **:param kwargs:** Diccionario 'clave':valor que recibe la referencia de la instancia del modelo proyecto.<br/>
        **:return:** el formulario , la plantilla donde se va desplegar el formulario de creación.<br/>
        """
        comite = get_object_or_404(Comite, pk=kwargs.get('pk'))
        form = self.form_class(request.POST or None, instance=comite)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        """

        Función que valida el formulario y lo guarda y redirige a una plantilla en caso de ser exitosa.<br/>
        **:param form:** Recibe el formulario.<br/>
        **:return:** Retorna la creación exitosa del formulario.<br/>
        """
        comite = form.save()
        return redirect(self.success_url)


# === delete comite ===
class DeleteComite(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """
    Permite suprimir una instancia del modelo de Comite.<br/>
    **:param PermissionRequiredMixin:** Libreria que gestiona el permiso para la creación de comite.El usuario
    debe poseer el permiso correspondiente de eliminar comite.<br/>
    **:param LoginRequiredMixin:** Requiere estar logueado, de la libreria django.contrib.auth.mixins<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Eliminar una instancia del modelo comite, luego se redirige a la lista de proyectos.<br/>
    """
    model = Comite
    template_name = 'comite/delete.html'
    permission_required = 'comite.eliminar_comite'
    success_url = reverse_lazy('proyecto:list')


# === detail comite ===
class DetailComite(LoginRequiredMixin, DetailView, PermissionRequiredMixin):
    """
    Despliega los detalles de una instancia del modelo de Proyecto.<br/>
    **:param PermissionRequiredMixin:** Libreria que gestiona el permiso para la creación de proyectos.El usuario
    debe poseer el permiso correspondiente de eliminar proyectos.<br/>
    **:param LoginRequiredMixin:** Requiere estar logueado, de la libreria django.contrib.auth.mixins<br/>
    **:param DetailView:** Recibe una vista generica de tipo DetailView para vistas basadas en clases.<br/>
    **:return:** Despliega los detalles de una instancia del modelo Proyecto.<br/>
    """
    model = Comite
    template_name = 'comite/detail.html'
    permission_required = 'comite.ver_comite'
    success_url = reverse_lazy('comite:detail')

# **Atras** : [[urls.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
