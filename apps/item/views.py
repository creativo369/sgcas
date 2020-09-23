import decimal
from datetime import date

import pyrebase

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
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
from apps.proyecto.models import Proyecto

from SGCAS.decorators import requiere_permiso
from SGCAS.settings.desarrollo import MEDIA_ROOT

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
    query_fase = Fase.objects.get(
        id=id_fase)  # Obtenemos la instancia de la fase para poder acceder desde ella hasta el estado del proyecto
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, id_fase=id_fase)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            fase = get_object_or_404(Fase, pk=id_fase)
            if Item.objects.filter(Q(nombre=nombre) & Q(fase=fase)).exists():
                return render(request, 'item/validate_item.html')

            item = form.save(commit=False)
            item.fase = Fase.objects.get(id=id_fase)
            item.save()
            form.save_m2m()

            ##Actualizamos la complejidad del proyecto
            proyecto = get_object_or_404(Proyecto, pk=fase.proyecto.pk)
            proyecto.complejidad += item.costo
            proyecto.save()

            if request.FILES:
                # ALMACENAMIENTO FIREBASE
                path_local = MEDIA_ROOT + '/' + item.archivo.name  # Busca los archivos en MEDIA/NOMBREARCHIVO
                path_on_cloud = str(
                    date.today()) + '/' + item.archivo.name  # Se almacena en Firebase como FECHADEHOY/NOMBREARCHIVO
                storage.child(path_on_cloud).put(path_local)  # Almacena el archivo en Firebase
                # print(storage.child(path_on_cloud).get_url(item.archivo.name))
                item.file_url_cloud = storage.child(path_on_cloud).get_url(item.archivo.name)
                item.save()
            return redirect('item:importar_tipo_item', pk=item.pk)
    elif query_fase.proyecto.estado == "Iniciado":  # Solamente cuando el proyecto este en estado iniciado se pueden crear los items
        form = ItemForm(id_fase=id_fase)
    else:
        return render(request, 'item/item_crear.html', {'validacion_proyecto': query_fase})
    return render(request, 'item/item_crear.html',
                  {'form': form, 'tipo_item': TipoItem.objects.exists(), 'validacion_proyecto': query_fase})


# === importar tipo de ítem ===
@requiere_permiso('importar_tipo_item')
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
@requiere_permiso('importar_tipo_item')
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
# @requiere_permiso('ver_item')
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


# @requiere_permiso('item.listar_item')
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
def item_eliminar(request, pk, id_fase):
    """
       Permite la eliminacion de uns instancia de objeto ítem.<br/>
       **:param request:** Recibe un request por parte de un usuario.<br/>
       **:param pk:** Recibe pk de la instancia del ítem que se desea eliminar.<br/>
       **:return:** Se elimina el ítem y se redirige a la lista de ítems de la fase.<br/>
       """
    item = Item.objects.get(id=pk)
    id_fase = item.fase.pk
    proyecto = get_object_or_404(Proyecto, pk=get_object_or_404(Fase, pk=id_fase).proyecto.pk)
    proyecto.complejidad -= item.costo
    proyecto.save()
    actualizar_punteros(item)
    item.delete()
    return redirect('item:item_lista', id_fase=id_fase)


##Actualiza los punteros de las relaciones
##Todos los padres apuntan a todos los hijos.
##Todos los hijos apuntan a todos los padres
##Todos los antecesores apuntan a todos los sucesores
##Todos los sucesores apuntan a tdos los antecesores
def actualizar_punteros(item):
    print("Actualizando punteros...")
    padres = item.padres.all()
    hijos = item.hijos.all()
    antecesores = item.antecesores.all()
    sucesores = item.sucesores.all()

    for hijo in hijos:
        for padre in padres:
            hijo.padres.add(padre)
    for padre in padres:
        for hijo in hijos:
            padre.hijos.add(hijo)
    for antecesor in antecesores:
        for sucesor in sucesores:
            antecesor.sucesores.add(sucesor)
    for sucesor in sucesores:
        for antecesor in antecesores:
            sucesor.antecesores.add(antecesor)


# === ítem detalles ===
@requiere_permiso('ver_item')
def item_detalles(request, pk, id_fase):
    """
       Permite visualizar los detalles de una instancia de ítem.<br/>
       **:param request:** Recibe un request por parte de un usuario.<br/>
       **:param pk:** Recibe pk de la instancia del ítem que se desea visualizar.<br/>
       **:return:** Se visualizan los detalles del ítem.<br/>
    """
    return render(request, 'item/item_detalles.html', {'item': Item.objects.get(pk=pk)})


@requiere_permiso('editar_item')
@requiere_permiso('item_modificar_ti')
@requiere_permiso('item_modificar_atributos')
# === ítem modificar ===
def item_modificar_basico(request, pk, id_fase):
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
        item.save()
        form.save_m2m()
        if request.FILES:
            item.archivo = request.FILES['archivo']
            # ALMACENAMIENTO FIREBASE
            path_local = MEDIA_ROOT + '/' + item.archivo.name  # Busca los archivos en MEDIA/NOMBREARCHIVO
            path_on_cloud = str(
                date.today()) + '/' + item.archivo.name  # Se almacena en Firebase como FECHADEHOY/NOMBREARCHIVO
            storage.child(path_on_cloud).put(path_local)  # Almacena el archivo en Firebase
            item.file_url_cloud = storage.child(path_on_cloud).get_url(item.archivo.name)
            item.save()
        return redirect('item:item_modificar_import_ti', pk=item.pk)
    context = {
        'form': form,
        'item': item,
        'tipo_item': TipoItem.objects.exists()
    }
    return render(request, 'item/item_modificar.html', context)



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
        file_url_cloud=prev_item.file_url_cloud,
        fase=prev_item.fase,
        tipo_item=prev_item.tipo_item,
        impacto=prev_item.impacto,
        # Atributos de tipo de item
        boolean=prev_item.boolean,
        char=prev_item.char,
        date=prev_item.date,
        numerico=prev_item.numerico,
        # Atributos de versionado
        nro_version=prev_item.nro_version,
        last_release=False,
        ultima_modificacion=prev_item.ultima_modificacion,
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
def item_versiones(request, pk, id_fase):
    lista_item_version = Item.objects.get(pk=pk).item_set.all().order_by('id')
    fase = Fase.objects.get(id=id_fase)

    paginator = Paginator(lista_item_version, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'versiones': lista_item_version,
        'fase': fase,
        # 'page_obj': page_obj
    }

    return render(request, 'item/item_versiones.html', context)


@requiere_permiso('versiones_item')
# === restaurar versión ===
def restaurar_version(request, pk, id_fase):
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
    prev_estado = item.estado
    if item.antecesores.all().exists() or item.sucesores.all().exists() or item.padres.all().exists() or item.hijos.all().exists():
        form = ItemCambiarEstado(request.POST or None, instance=item)
        if form.is_valid():
            lb = get_lb(pk)
            new_estado = form.cleaned_data['estado']
            if prev_estado == 'Aprobado' and new_estado == 'Desarrollo':
                if lb is not None and lb.estado == 'Cerrada':
                    return redirect('comite:solicitud_linea_base', pk)
                return redirect('comite:solicitud_item', pk)
            form.save()
            return redirect('item:item_lista', id_fase=item.fase.pk)
        return render(request, 'item/item_cambiar_estado.html', {'form': form, 'item': item})
    return render(request, 'item/item_cambiar_estado.html', {'item': item})
    

##Retorna la linea base de item (si tiene)
def get_lb(pk):
    item = Item.objects.get(pk=pk)
    for lb in LineaBase.objects.all():
        if item in lb.items.all():
            return lb
    return None


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
        items_query = Item.objects.filter(Q(fase=item.fase) & Q(last_release=True)).exclude(pk=item.pk)
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
        items_query = Item.objects.filter(Q(fase=to_fase) & Q(last_release=True))
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
        items_query = Item.objects.filter(Q(fase=to_fase) & Q(last_release=True))
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
    item = get_object_or_404(Item, pk=pk)
    complejidad_proyecto = get_object_or_404(Fase, pk=item.fase.pk).proyecto.complejidad
    calculo = explore(item, impacto=0)
    context = {
        'complejidad_proyecto':complejidad_proyecto, 
        'item':item,
        'calculo_impacto':round((calculo/complejidad_proyecto), 2)
    }
    return render(request, 'item/item_calculo_impacto.html', context)


def explore(item, impacto):
    """
    Explora el arbol sumando los costos.<br/>
    **:param item:** El item del cual se desea averiguar el calculo de impacto.<br/>
    **:param impacto:** Variable recursiva utilizada para compartir entre las llamadas.<br/>
    **:return:** El impacto de un item en el proyecto.<br/>
    """
    impacto += item.costo
    for hijo in item.hijos.all():
        return explore(hijo, impacto)
    for sucesor in item.sucesores.all():
        return explore(sucesor, impacto)
    return impacto


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
