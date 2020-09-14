import decimal
from datetime import date

import pyrebase

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView
from guardian.mixins import PermissionRequiredMixin

from apps.fase.models import Fase
from apps.item.forms import ItemForm, ItemUpdateForm, ItemImportarTipoItemForm, ItemAtributosForm, ItemCambiarEstado, \
    RelacionForm
from apps.item.graph import exclude_potencial_cycles, shortest_path, create_graph_trazabilidad, draw_graph, \
    item_has_path
from apps.item.models import Item
from apps.linea_base.models import LineaBase
from apps.tipo_item.models import TipoItem

from SGCAS.decorators import requiere_permiso

firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
storage = firebase.storage()

"""
Todas las vistas para la aplicación del Modulo ítem
Actualmente se despliega en las plantillas 19 vistas:
1. **crear_item_basico** - crea el ítem (Ir a la sección: [[views.py #crear ítem]] )
2. **item_importar_ti** - asigna un tipo de ítema al item (Ir a la sección: [[views.py #importar tipo de ítem]] )
3. **item_set_atributos** - asigna al ítem sus atributos (Ir a la sección: [[views.py #settear atributos ítem]] )
4. **item_lista_fase** - lista los ítems de una fase (Ir a la sección: [[views.py #lista de ítems de fase]] )
5. **search** - lista los ítems buscados en una fase (Ir a la sección: [[views.py #search]] )
6. **item_eliminar** - elimina un ítem permanentemente (Ir a la sección: [[views.py #ítem eliminar]] )
7. **item_detalles** - despliega información relevante sobre un ítem (Ir a la sección: [[views.py #ítem detalles]] )
8. **item_modificar_basico** - modifica los atributos de un ítem (Ir a la sección: [[views.py #ítem modificar]] )
9. **item_modificar_ti** - modifica el tipo de ítem que posee un ítem (Ir a la sección: [[views.py #modificar ti]] )
10. **item_modificar_atributos** - modifica los atributos del tipo de ítem que posee un ítem (Ir a la sección: [[views.py #ítem modificar atributos]] )
11. **get_item_snapshot** - almacena una copia de ítem, es su versión actual (Ir a la sección: [[views.py #snapshot ítem]] )
12. **item_versiones** - lista todas las versiones que posee un ítem (Ir a la sección: [[views.py #ítem versiones]] )
13. **restaurar_version** - regresa el ítem a una versión anterior a la actual (Ir a la sección: [[views.py #restaurar versión]] )
14. **item_cambiar_estado** - modifica el estado de un ítem (Ir a la sección: [[views.py #ítem cambiar estado]] )
15. **fases_rel** - despliega las fases que contienen a los ítems para relacionarlos (Ir a la sección: [[views.py #fases relaciones]] )
16. **get_context** - vista que crea un diccionario de ítems (Ir a la sección: [[views.py #contexto ítem]] )
17. **relaciones** - efectúa el relacionamiento de los ítems (Ir a la sección: [[views.py #relaciones]] )
18. **calculo_impacto** - efectúa el cálculo del impacto, que tendría sobre el proyecto la modificación del ítem (Ir a la sección: [[views.py #impacto ítem]] )
19. **trazabilidad_item** - representa en forma gráfica las relaciones que posee un ítem (Ir a la sección: [[views.py #impacto ítem]] )
"""



# @permission_required('item.crear_item', raise_exception=True)
# === crear ítem ===
@requiere_permiso('crear_item')
def crear_item_basico(request, id_fase):

    """
    Permite la creacion de instancias de modelo Item.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:**  Retorna una instancia del modelo Item.<br/>
    """
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, id_fase=id_fase)
        if form.is_valid():
            item = form.save(commit=False)
            item.fase = Fase.objects.get(id=id_fase)
            item.save()
            form.save_m2m()

            if request.FILES:
                ##ALMACENAMIENTO FIREBASE
                path_local = 'deployment/media/' + item.archivo.name  # Busca los archivos en MEDIA/NOMBREARCHIVO
                path_on_cloud = str(
                    date.today()) + '/' + item.archivo.name  # Se almacena en Firebase como FECHADEHOY/NOMBREARCHIVO
                storage.child(path_on_cloud).put(path_local)  # Almacena el archivo en Firebase
                # print(storage.child(path_on_cloud).get_url(item.archivo.name))
                item.file_url_cloud = storage.child(path_on_cloud).get_url(item.archivo.name)
                item.save()
            return redirect('item:importar_tipo_item', pk=item.pk)
    else:
        form = ItemForm(id_fase=id_fase)

    return render(request, 'item/item_crear.html', {'form': form, 'tipo_item': TipoItem.objects.exists()})


@requiere_permiso('importar_tipo_item')
# === importar tipo de ítem ===
def item_importar_ti(request, pk):
    """
    Permite la creacion de instancias de modelo Ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de ítem a la cual se le asignara el tipo de ítem.<br/>
    **:return:**  Retorna una instancia de ítem con su tipo de ítem agregado.<br/>
    """
    item = get_object_or_404(Item, pk=pk)
    form = ItemImportarTipoItemForm(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save()
        return redirect('item:set_atributos', pk=item.id)
    return render(request, 'item/item_importar_tipo_item.html', {'form': form,
                                                                 'tipo_item': TipoItem.objects.all().exists(),
                                                                 'fase': item.fase})


# === settear atributos ítem ===
@requiere_permiso('crear_item')
def item_set_atributos(request, pk):
    """
    Permite agregar los atributos a un ítem de acuerdo a su tipo de ítem importado.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de ítem al cual se le asignará los atributos.<br/>
    **:return:**  Retorna una instancia de ítem con sus atributos agregados.<br/>
    """
    item = get_object_or_404(Item, pk=pk)
    form = ItemAtributosForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item:item_lista', id_fase=Item.objects.get(id=pk).fase.pk)
    return render(request, 'item/item_atributos_tipo_item.html', {'form': form,
                                                                  'fase': item.fase})


@login_required
@requiere_permiso('ver_item')
# === ítem opciones ===
def item_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo Ítem.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema.<br/>
    """

    return render(request, 'item/item_opciones.html')


@requiere_permiso('listar_item')
# === lista de ítems de fase ===
def item_lista_fase(request, id_fase):
    """
    Permite visualizar todos los ítems de una fase en particular.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de la fase del cual se desea visualizar los ítems.<br/>
    **:return:**  Retorna una lista de ítems correspondientes a la fase.<br/>
    """
    lista_item = Item.objects.filter(Q(last_release=True) & Q(fase=Fase.objects.get(id=id_fase))).order_by(
        'id').distinct()
    fase = Fase.objects.get(id=id_fase)
    paginator = Paginator(lista_item, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': Item.objects.filter(fase=Fase.objects.get(id=id_fase)).filter(last_release=True),
        'proyecto': Fase.objects.get(id=id_fase).proyecto,
        'page_obj': page_obj,
        'fase': fase
    }

    return render(request, 'item/item_lista.html', context)


@requiere_permiso('item.listar_item')
# === search ===
def search(request, id_fase):
    """
    Permite realizar la búsqueda de ítems de una fase.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de la fase del cual se desea visualizar los ítems.<br/>
    **:return:**  Retorna los ítems  de una fase, que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'item/list_busqueda.html'
    query = request.GET.get('buscar')
    proyecto = Fase.objects.get(id=id_fase).proyecto
    fase = Fase.objects.get(id=id_fase)

    if query:
        results = Item.objects.filter(Q(last_release=True) & Q(fase=Fase.objects.get(id=id_fase)) &
                                      (Q(nombre__icontains=query) | Q(descripcion__contains=query))).order_by(
            'id').distinct()
    else:
        results = Item.objects.filter(Q(last_release=True) & Q(fase=Fase.objects.get(id=id_fase))).order_by(
            'id').distinct()

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'items': results,
        'proyecto': proyecto,
        'page_obj': page_obj,
        'fase': fase
    }

    return render(request, template, context)


@requiere_permiso('eliminar_item')
# === ítem eliminar ===
def item_eliminar(request, pk):
    """
       Permite la eliminacion de uns instancia de objeto ítem.<br/>
       **:param request:** Recibe un request por parte de un usuario.<br/>
       **:param pk:** Recibe pk de la instancia del ítem que se desea eliminar.<br/>
       **:return:** Se elimina el ítem y se redirige a la lista de ítems de la fase.<br/>
       """
    item = Item.objects.get(id=pk)
    id_fase = item.fase.pk
    item.delete()
    return redirect('item:item_lista', id_fase=id_fase)


# === ítem detalles ===
@requiere_permiso('ver_item')
def item_detalles(request, pk):
    """
       Permite visualizar los detalles de una instancia de ítem.<br/>
       **:param request:** Recibe un request por parte de un usuario.<br/>
       **:param pk:** Recibe pk de la instancia del ítem que se desea visualizar.<br/>
       **:return:** Se visualizan los detalles del ítem.<br/>
    """
    return render(request, 'item/item_detalles.html', {'item': Item.objects.get(pk=pk)})


@requiere_permiso('editar_item')
# === ítem modificar ===
def item_modificar_basico(request, pk):
    """
    Permite la modificación de una instancia de ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del ítem que se desea modificar.<br/>
    **:return:**  Retorna una instancia de un item con sus configuraciones basicas modificadas.<br/>
    """
    item = get_object_or_404(Item, pk=pk)
    fase = item.fase
    l_base = LineaBase.objects.filter(fase=fase)
    l_base = [lb for lb in l_base if
              lb.items.filter(pk=item.pk).exists()]  # Se obtiene la linea base a la cual pertenece el item
    if l_base and l_base[0].estado == 'Cerrada':
        l_base = l_base[0]
        # return render(request, 'item/item_solicitud.html', {})
    form = ItemUpdateForm(request.POST or None, instance=item, id_fase=fase.pk)
    if form.is_valid():
        version_item = get_item_snapshot(pk)
        item = form.save(commit=False)
        item.nro_version += decimal.Decimal(0.1)  ##Adjunta numero de versión
        item.item_set.add(version_item)
        for i in version_item.item_set.all():
            item.item_set.add(i)
        form.save()
        return redirect('item:item_modificar_import_ti', pk=item.pk)
    return render(request, 'item/item_modificar.html', {'form': form, 'tipo_item': TipoItem.objects.exists()})


@requiere_permiso('item_modificar_ti')
# === modificar ti ===
def item_modificar_ti(request, pk):
    """
    Permite la modificación del tipo de ítem de un ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del item que se desea modificar.<br/>
    **:return:** Retorna una instancia de un ítem con su tipo de ítem modificado.<br/>
    """
    item = get_object_or_404(Item, pk=pk)
    form = ItemImportarTipoItemForm(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save()
        return redirect('item:item_modificar_atr_ti', pk=item.pk)
    return render(request, 'item/item_importar_tipo_item.html', {'form': form, 'fase': item.fase, 'item': item})


@requiere_permiso('item_modificar_atributos')
# === ítem modificar atributos ===
def item_modificar_atributos(request, pk):
    """
    Permite la modificación de los atributos de un tipo de ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del ítem que se desea modificar.<br/>
    **:return:** Retorna una instancia de un ítem con sus atributos modificados.<br/>
    """
    item = get_object_or_404(Item, pk=pk)
    form = ItemAtributosForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item:item_lista', id_fase=item.fase.pk)
    return render(request, 'item/item_atributos_tipo_item.html', {'form': form})


# === snapshot ítem ===
def get_item_snapshot(pk):
    """
    Permite guardar el estado de un ítem.<br/>
    **:param pk:** Recibe pk de una instancia del ítem del cual se desea guardar su estado.<br/>
    **:return:** Retorna una instancia de ítem que es la copia del ítem recibido.<br/>
    """
    print('Taking snapshot...')
    prev_item = get_object_or_404(Item, pk=pk)
    snap_item = Item.objects.create(
        nombre=prev_item.nombre,
        descripcion=prev_item.descripcion,
        fecha_creacion=prev_item.fecha_creacion,
        estado=prev_item.estado,
        costo=prev_item.costo,
        archivo=prev_item.archivo,
        fase=prev_item.fase,
        tipo_item=prev_item.tipo_item,
        # Atributos de tipo de item
        boolean=prev_item.boolean,
        char=prev_item.char,
        date=prev_item.date,
        numerico=prev_item.numerico,
        # Atributos de versionado
        nro_version=prev_item.nro_version,
        ultima_modificacion=prev_item.ultima_modificacion,
        last_release=False
    )
    ## Atributo basico
    snap_item.usuarios_a_cargo.add(*prev_item.usuarios_a_cargo.all())
    ## Atributos para relaciones ###
    snap_item.padres.add(*prev_item.padres.all())
    snap_item.hijos.add(*prev_item.hijos.all())
    snap_item.antecesores.add(*prev_item.antecesores.all())
    snap_item.sucesores.add(*prev_item.sucesores.all())
    ## Atributos para el versionado
    snap_item.item_set.add(*prev_item.item_set.all())

    return snap_item


@requiere_permiso('versiones_item')
# === ítem versiones ===
def item_versiones(request, pk, id_fases):
    lista_item_version = Item.objects.get(pk=pk).item_set.all().order_by('id')
    fase = Fase.objects.get(id=id_fases)

    paginator = Paginator(lista_item_version, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # 'versiones_queryset': lista_item_version,
        'fase': fase,
        'page_obj': page_obj
    }

    return render(request, 'item/item_versiones.html', context)


@requiere_permiso('versiones_item')
# === restaurar versión ===
def restaurar_version(request, pk):
    """
    Permite la restauración de la versión de un ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del ítem el cual representa la versión a la cual se desea regresar.<br/>
    **:return:** Retorna una instancia de ítem actualizada.<br/>
    """
    nr_item = Item.objects.get(pk=pk)  ##new release item
    lr_item = Item.objects.get(pk=nr_item.versiones.pk)  ##latest release item

    if request.method == 'POST':
        nr_item.versiones = None
        oldest_version_query = lr_item.item_set.filter(nro_version__lt=nr_item.nro_version)

        ##Se redirecciona el historial al nuevo last_release
        ##Y se elimina la relación de foreign key con el anterior last release
        ##porque de otra forma se eliminarian
        for older_version in oldest_version_query:
            older_version.versiones = nr_item
            older_version.save()
        nr_item.last_release = True  ##Ahora la ultima version es la version elegida
        nr_item.save()
        ##Se eliminan las versiones posteriores
        lr_item.delete()  ##Se borra la ultima version y por consiguiente las foreign key mayores que la version elegida

        return redirect('item:item_lista', id_fase=nr_item.fase.pk)
    return render(request, 'item/item_eliminar.html', {'object': nr_item})


@requiere_permiso('cambiar_estado_item')
# === ítem cambiar estado ===
def item_cambiar_estado(request, pk):
    """
    Permite la modificación del estado de un ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del ítem que se desea modificar.<br/>
    **:return:** Retorna una instancia de un ítem con su estado modificado.<br/>
    """
    item = get_object_or_404(Item, pk=pk)
    form = ItemCambiarEstado(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item:item_lista', id_fase=item.fase.pk)
    return render(request, 'item/item_cambiar_estado.html', {'form': form, 'item': item})


# === fases relaciones ===
@requiere_permiso('relacion_item')
def fases_rel(request, pk):
    """
    Permite la visualización de las fases de un ítem, paso previo para establecer de las relaciones.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del ítem, ejecutor de la acción de 'establecer relación'.<br/>
    **:return:** Retorna un template de las fases de un proyecto.<br/>
    """
    proyecto = Item.objects.get(pk=pk).fase.proyecto
    context = {
        'item': get_object_or_404(Item, pk=pk),
        'fase': get_object_or_404(Item, pk=pk).fase,
        'fases_proyecto': Fase.objects.filter(proyecto=proyecto),
    }
    return render(request, 'item/item_fases_relaciones.html', context)


##Obtiene el contexto para el template de las relaciones
# === contexto ítem ===
def get_context(form, items_query, item_pk, fase_pk):
    """
    Realiza el proceso para la obtencion del contexto que se utiliza en la funcion de 'relaciones'.<br/>
    **:param form:** Recibe el formulario de entrada.<br/>
    **:param items_query:** Recibe el queryset de ítems disponibles para las relaciones.<br/>
    **:param item_pk:** Recibe el pk del ítem ejecutor de 'Establecer relación'.<br/>
    **:param fase_pk:** Recibe el pk de la fase al cual el ítem ejecutor desea establecer la relación.<br/>
    **:return:** Retorna contexto en formato diccionario de los parametros dados.<br/>
    """
    context = {
        'form': form,
        'items_query': items_query,
        'item': get_object_or_404(Item, pk=item_pk),
        'fase': Fase.objects.get(pk=fase_pk)
    }

    return context


# === update relations ===
def update_relations(pk, snap_pk):
    snap_item = get_object_or_404(Item, pk=snap_pk)
    new_item = get_object_or_404(Item, pk=pk)

    # for hijo in snap_item.hijos.all():


@requiere_permiso('relacion_item')
# === relaciones ===
def relaciones(request, pk, id_fase):
    """
    Permite establecer relaciones entre instancias de un ítem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia del ítem, ejecutor de la acción 'establecer relación'.<br/>
    **:return:** Retorna una instancia de ítem con sus relaciones actualizadas.<br/>
    """
    ## flags: -1 para antecesores, 0 para hijos, 1 para sucesores
    from_fase = get_object_or_404(Item, pk=pk).fase.id  # Id de la fase a la cual corresponde el item
    to_fase = int(id_fase)  # id de la fase a la cual se desea direccionar la relacion
    item = get_object_or_404(Item, pk=pk)
    if from_fase == to_fase:  ##Relaciones padre/hijos
        items_query = Item.objects.filter(fase=Item.objects.get(pk=pk).fase.id).exclude(pk=pk)
        for item_p in items_query:  # Se exluyen los padres, un hijo no puede ser padre a la vez con respecto a un item
            if item in item_p.hijos.all():
                items_query = items_query.exclude(pk=item_p.pk)
        items_query = exclude_potencial_cycles(pk, id_fase, items_query)
        form = RelacionForm(request.POST or None, instance=get_object_or_404(Item, pk=pk), query=items_query, flag=0)
        if form.is_valid():
            older_version_item = get_item_snapshot(pk)
            _item = form.save()
            for hijo in older_version_item.hijos.all():
                if not _item.hijos.all().filter(pk=hijo.pk).exists():
                    hijo.padres.remove(_item)
            for hijo in _item.hijos.all():
                hijo.padres.add(_item)
            ##update_relations
            older_version_item.delete()
            return redirect('item:item_lista', id_fase=Item.objects.get(pk=pk).fase.pk)
        context = get_context(form, items_query, pk, id_fase)
        return render(request, 'item/item_relaciones.html', context)
    elif from_fase > to_fase:  ##Relacion antecesores <- item
        items_query = Item.objects.filter(fase=to_fase)
        items_query = exclude_potencial_cycles(pk, id_fase, items_query)
        form = RelacionForm(request.POST or None, instance=get_object_or_404(Item, pk=pk), query=items_query, flag=-1)
        if form.is_valid():
            older_version_item = get_item_snapshot(pk)
            _item = form.save()
            # form.save()
            for antecesor in older_version_item.antecesores.all():
                if not _item.antecesores.all().filter(pk=antecesor.pk).exists():
                    antecesor.sucesores.remove(_item)
            for antencesor in _item.antecesores.all():  ##Setea los sucesores
                antencesor.sucesores.add(_item)
            ##update_rel
            older_version_item.delete()
            return redirect('item:item_lista', id_fase=Item.objects.get(pk=pk).fase.pk)
        context = get_context(form, items_query, pk, id_fase)
        return render(request, 'item/item_relaciones.html', context)
    else:  ##Relacion item -> sucesores
        items_query = Item.objects.filter(fase=to_fase)
        items_query = exclude_potencial_cycles(pk, id_fase, items_query)
        form = RelacionForm(request.POST or None, instance=get_object_or_404(Item, pk=pk), query=items_query, flag=1)
        if form.is_valid():
            older_version_item = get_item_snapshot(pk)
            _item = form.save()
            # form.save()
            for sucesor in older_version_item.sucesores.all():
                if not _item.sucesores.all().filter(pk=sucesor.pk).exists():
                    sucesor.antecesores.remove(_item)
            for sucesor in _item.sucesores.all():  ##Setea los sucesores
                sucesor.antecesores.add(_item)
            ##update_rel
            older_version_item.delete()
            return redirect('item:item_lista', id_fase=Item.objects.get(pk=pk).fase.pk)
        context = get_context(form, items_query, pk, id_fase)
        return render(request, 'item/item_relaciones.html', context)


@requiere_permiso('calcular_impacto')
# === impacto ítem ===
def calculo_impacto(request, pk):
    """
    Permite realizar el cálculo de impacto de un ítem al proyecto.<br/>
    **:param request:** Recibe un request por parte del usuario.<br/>
    **:param pk:** Recibe el pk de una instancia de ítem sobre el cual se le realizará el cálculo de impacto.<br/>
    **:return:** El cálculo de impacto de un ítem en terminos numericos.<br/>
    """
    target = Item.objects.get(pk=pk)
    fase = Fase.objects.filter(proyecto=target.fase.proyecto).first()
    source = Item.objects.filter(fase=fase).filter(last_release=True).earliest(
        'id')  ##Se toma como el source el primer item del proyecto
    if item_has_path(fase.pk, source, target):
        path = shortest_path(source, target, fase.pk)
        for item in path:  ##Se calcula del impacto en cada item del path
            if path.index(item) == 0:
                item.impacto = item.costo
            else:
                item.impacto = item.costo + path[path.index(item) - 1].impacto
            item.save()
        context = {'target': target, 'path': shortest_path(source, target, fase.pk)}
    else:
        context = {'target': target}
    return render(request, 'item/item_calculo_impacto.html', context)


@requiere_permiso('ver_trazabilidad')
# === trazabilidad ítem ===
def trazabilidad_item(request, pk):
    """
    Permite obtener la trazabilidad de un item.<br/>
    **:param request:** Recibe un request por parte del usuario.<br/>
    **:param pk:** Recibe el pk de una instancia de item sobre el cual se realizara la trazabilidad.<br/>
    **:return:** La trazabilidad de un ítem (Si posee) en formato .png renderizado en el template.<br/>
    """
    target = Item.objects.get(pk=pk)
    fase = Fase.objects.filter(proyecto=target.fase.proyecto).first()
    source = Item.objects.filter(fase=fase).filter(last_release=True).earliest('id')
    if item_has_path(fase.pk, source, target):
        G = create_graph_trazabilidad(shortest_path(source, target, fase.pk))
        draw_graph(G)
        context = {
            'image_name': 'item_trazabilidad.png',
            'item_name': target.nombre
        }
    else:
        context = {
            'item_name': target.nombre
        }
    return render(request, 'item/item_trazabilidad.html', context)


# class ItemLista(ListView, PermissionRequiredMixin, LoginRequiredMixin):
#     """
#     Permite la visualizacion en lista de todas las intancias del modelo Item<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.<br/>
#     **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
#     **:param LoginRequiredMixin:** Acceso controlado por logueo, de la libreria auth.mixins.<br/>
#     **:return:** Una vista de todas las intancias a traves del archivo item_lista.html.<br/>
#     """
#     paginate_by = 4
#     model = Item
#     template_name = 'item/item_lista.html'
#     permission_required = 'item.ver_item'

#     # La lista a mostrar estara por orden ascendente
#     class Meta:
#         ordering = ['-id']


# class ItemEliminar(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):
#     """
#     Permite la eliminacion instancias de modelos Item.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.<br/>
#     **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
#     **:param LoginRequiredMixin:** Acceso controlado por logueo, de la libreria auth.mixins.<br/>
#     **:return:** Elimina una instancia del modelo Item del sistema.<br/>
#     """
#     model = Item
#     template_name = 'item/item_eliminar.html'
#     permission_required = 'item.eliminar_item'
#     success_url = reverse_lazy('item:item_lista')


# class ItemModificar(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
#     """
#     Permite la modificacion de informacion basica de una instancia de modelo Item.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria guardian.mixins.<br/>
#     **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
#     **:param LoginRequiredMixin:** Acceso controlado por logueo, de la libreria auth.mixins.<br/>
#     **:return:** Modficia una instancia del modelo Item, luego se redirige para la importacion de Tipo de Item.<br/>
#     """
#     model = Item
#     template_name = 'item/item_crear.html'
#     form_class = ItemUpdateForm
#     permission_required = 'item.editar_item'

#     def form_valid(self, form):
#         object = form.save()
#         return redirect('item:item_modificar_import_ti', pk=object.pk)


# class ItemModificarImportTI(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
#     """
#     Permite la modificacion de importacion de Tipo de Item de una instancia de modelo Item.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria guardian.mixins.<br/>
#     **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
#     **:param LoginRequiredMixin:** Acceso controlado por logueo, de la libreria auth.mixins.<br/>
#     **:return:** Modifica una instancia del modelo Item, luego se redirige para setear los atrobutos del Tipo de Item importado<br/>
#     """
#     model = Item
#     template_name = 'item/item_importar_tipo_item.html'
#     form_class = ItemImportarTipoItemForm
#     permission_required = 'item.item_modificar_import_ti'

#     def form_valid(self, form):
#         object = form.save()
#         return redirect('item:item_modificar_atr_ti', pk=object.pk)


# class ItemModificarAtrTI(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
#     """
#     Permite la modificacion de atributos de una instancia de modelo Item.<br/>
#     **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria guardian.mixins.<br/>
#     **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
#     **:param LoginRequiredMixin:** Acceso controlado por logueo, de la libreria auth.mixins.<br/>
#     **:return:** Modifica na instancia del modelo Item, luego se redirige a la lista de items.<br/>
#     """
#     model = Item
#     template_name = 'item/item_atributos_tipo_item.html'
#     form_class = ItemAtributosForm
#     permission_required = 'item.item_modificar_atributos_ti'
#     success_url = reverse_lazy('item:item_lista')

# **Atras** : [[urls.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)