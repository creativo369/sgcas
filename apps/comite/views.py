# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from SGCAS.settings import base



# === Importación de los codigos fuentes de la aplicación ===
from .models import Comite, Solicitud
from .forms import FormularioComite, FormularioComiteUpdate, FormularioSolicitud
from ..proyecto.models import Proyecto
from apps.item.models import Item
from apps.linea_base.models import LineaBase
from apps.item.views import get_lb

"""
Todas las vistas para la aplicación del Modulo Comité
Actualmente se despliega en las plantillas 13 vistas:

1. **success** - operación exitosa para la creación de un comite (Ir a la sección: [[views.py #success]] )
2. **CreateComite** - definición de una instancia del modelo comité (Ir a la sección: [[views.py #create comite]] )
3. **UpdateComite** - modificar una instancia del modelo comité (Ir a la sección: [[views.py #update comite]] )
4. **DeleteComite** - suprimir una instancia del modelo comité (Ir a la sección: [[views.py #delete comite]] )
5. **DetailComite** - ver detalles de una instancia del modelo comité (Ir a la sección: [[views.py #detail comite]] )

6. **voto_favor** - registra los votos a favor de la solicitud de cambio (Ir a la sección: [[views.py #voto a favor]] )
7. **voto_contra** - registra los votos en contra de la solicitud de cambio (Ir a la sección: [[views.py #voto en contra]] )
8. **revision_votacion** - determina que opción obtiene la mayoria de votos (Ir a la sección: [[views.py #revision votacion]] )
9. **decision_comite** - notifica al solicitante la decision del comité (Ir a la sección: [[views.py #decision comite]] )
10. **lista_solicitudes** - lista las solicitudes que deben ser votadas (Ir a la sección: [[views.py #lista de solicitudes]] )
11. **solicitud_item** - remite la solicitud de cambio del ítem al comité (Ir a la sección: [[views.py #solicitud de ítem]] )
12. **solicitud_linea_base** - remite la solicitud de rotura de la linea base al comité (Ir a la sección: [[views.py #socilitud de linea base]] )
13. **send_notification** - se ecarga del envío de los correos al usuario solicitante (Ir a la sección: [[views.py #enviar correo]] )

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
    # permission_required = 'comite.crear_comite'
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

# @permission_required('comite.ver_comite', raise_exception=True)
# === voto a favor ===
def voto_favor(request, pk):
    """
    Realiza la votacion a favor de la aprobacion del artefacto.
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe el pk de la instancia de artefacto a ser votado.<br/>
    **:return:** Retorna al template de solicitudes del comite.<br/>
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.votacion += 1
    solicitud.votantes.add(request.user)
    solicitud.save()
    if revision_votacion(solicitud):
        decision_comite(solicitud)
    return redirect('comite:solicitudes', pk=Comite.objects.get(proyecto=solicitud.proyecto).pk)

# @permission_required('comite.ver_comite', raise_exception=True)
# === voto en contra ===
def voto_contra(request, pk):
    """
    Realiza la votacion en contra de la aprobacion del artefacto.
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe el pk de la instancia de artefacto a ser votado.<br/>
    **:return:** Retorna al template de solicitudes del comite.<br/>
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.votacion -= 1
    solicitud.votantes.add(request.user)
    solicitud.save()
    if revision_votacion(solicitud):
        decision_comite(solicitud)
    return redirect('comite:solicitudes', pk=Comite.objects.get(proyecto=solicitud.proyecto).pk)



##Revisa la votacion para ver si ya votaron todos los miembros, si ya votaron todos
# === revision votacion ===
def revision_votacion(solicitud):
    """
    Realiza la revision de la votacion.
    **:param solicitud:** Recibe la instancia de solicitud sobre la cual se hara la revision de la votacion.<br/>
    **:return:** Retorna True si todos los miembros del comite ya votaron, en caso contrario retorna False.<br/>
    """
    cant_miembros_comite=Comite.objects.get(proyecto=solicitud.proyecto).miembros.all().count()
    cant_votantes_solicitud=solicitud.votantes.all().count()
    if cant_miembros_comite > cant_votantes_solicitud:
        return False
    return True



# === decision comite ===
def decision_comite(solicitud):
    """
    Realiza la decision sobre el artefacto de acuerdo al resultado de la votacion, notificando por correo al solicitante sobre el resultado.
    **:param solicitud:** Recibe una instancia de solicitud sobre el cual se hara la decision de aprobar o no.<br/>
    **:return:** Retorna el artefacto aprobado si la votacion resulta a favor, en caso contrario, el artefacto no modifica su estado.<br/>
    """
    subject = ''
    message = ''
    if solicitud.votacion >= 1:
        subject = 'Solicitud aprobada.'
        if solicitud.item is not None:
            item = solicitud.item
            item.estado = 'Desarrollo'
            item.save()
            message = 'Su solicitud correspondiente al item {} ha sido aprobada por el comité.\n\nSGCAS.'.format(solicitud.item)
        else:
            lb = solicitud.linea_base
            lb.estado = 'Rota'
            lb.save()
            message = 'Su solicitud correspondiente a la linea base {} ha sido aprobada por el comité.\n\nSGCAS.'.format(solicitud.linea_base)
    else:
        subject = 'Solicitud no aprobada.'
        if solicitud.item is not None:
            message = 'Su solicitud correspondiente al item {} no ha sido aprobada por el comité.\n\nSGCAS.'.format(solicitud.item)
        else:
            message = 'Su solicitud correspondiente a la linea base {} no ha sido aprobada por el comité.\n\nSGCAS.'.format(solicitud.linea_base)
    send_notification(solicitud.solicitante.email, subject, message)
    solicitud.delete()


# @permission_required('comite.ver_solicitud', raise_exception=True)
# === lista de solicitudes ===
def lista_solicitudes(request, pk):
    """
    Renderiza la lista de solicitudes que se encuentran en proceso de votacion.
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe el pk de la instancia de comite, del cual se desea renderizar las solicitudes.<br/>
    **:return:** Retorna el template de solicitudes en proceso del comite de instancia.<br/>
    """
    solicitud = Solicitud.objects.filter(proyecto=Comite.objects.get(pk=pk).proyecto).order_by('id')

    paginator = Paginator(solicitud, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        #'solicitudes': Solicitud.objects.filter(proyecto=Comite.objects.get(pk=pk).proyecto),
        'miembro_comite': request.user,
        'comite':Comite.objects.get(pk=pk),
        'page_obj': page_obj
    }

    return render(request, 'comite/solicitudes.html', context)


@permission_required('comite.crear_solicitud', raise_exception=True)
# === solicitud de ítem ===
def solicitud_item(request, pk):
    """
    Realiza la solicitud del usuario para la modificacion de un item.
    **:param request:** Recibe un request por parte del usuario que realiza la solicitud.<br/>
    **:param pk:** Recibe el pk de la instancia de item que el usuario desea modificar.<br/>
    **:return:** Retorna al template de lista de items.<br/>
    """
    #Tipo solicitud: 0 para aprobacion de item, 1 para rotura de fase
    form = FormularioSolicitud(request.POST or None, pk=pk, request=request, tipo=0)
    if request.method == 'GET':
        context = {
            'form':form,
            'solicitud_en_proceso': Solicitud.objects.filter(item=get_object_or_404(Item, pk=pk)).count()
        }
        return render(request, 'comite/solicitud.html', context)
    else:
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.proyecto = get_object_or_404(Item, pk=pk).fase.proyecto
            solicitud.save()
            for miembro_comite in Comite.objects.get(proyecto=solicitud.item.fase.proyecto).miembros.all():
                message='{}:\n\nSe realizó una petición de aprobación para un item con el siguiente mensaje personalizado:\n{}\n\nSGCAS'.format(miembro_comite, solicitud.descripcion)
                send_notification(miembro_comite.email, solicitud.asunto, message)
            return redirect('item:item_lista', id_fase=Item.objects.get(pk=pk).fase.pk)


@permission_required('comite.crear_solicitud', raise_exception=True)
# === socilitud de linea base ===
def solicitud_linea_base(request, pk):
    """
    Realiza la solicitud del usuario para la rotura de la linea base.
    **:param request:** Recibe un request por parte del usuario que realiza la solicitud.<br/>
    **:param pk:** Recibe el pk de la instancia de item donde se encuentra la linea base que se desea romper.<br/>
    **:return:** Retorna al template de lista de items.<br/>
    """
    #Tipo solicitud: 0 para aprobacion de item, 1 para rotura de fase
    form = FormularioSolicitud(request.POST or None, pk=pk, request=request, tipo=1)
    if request.method == 'GET':
        context = {
            'form':form,
            'solicitud_en_proceso': Solicitud.objects.filter(linea_base=get_lb(pk)).count()
        }
        return render(request, 'comite/solicitud.html', context)
    else:
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.proyecto = get_object_or_404(Item, pk=pk).fase.proyecto
            solicitud.save()
            for miembro_comite in Comite.objects.get(proyecto=solicitud.item.fase.proyecto).miembros.all():
                message='{}:\n\nSe realizó una petición de aprobación para un item con el siguiente mensaje personalizado:\n{}\n\nSGCAS'.format(miembro_comite, solicitud.descripcion)
                send_notification(miembro_comite.email, solicitud.asunto, message)
            return redirect('item:item_lista', id_fase=Item.objects.get(pk=pk).fase.pk)


##Envia el correo
# === enviar correo ===
def send_notification(to, subject, message):
    """
    Realiza el envio de correo electronico.
    **:param to:** Destinatario del correo.<br/>
    **:param subject:** Asunto del correo.<br/>
    **:param message:** Mensaje a enviar al destinatario.<br/>
    """
    send_mail(
        subject,
        message,
        base.EMAIL_HOST_USER,
        [to, base.EMAIL_HOST_USER],
        fail_silently=False,
    )


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
