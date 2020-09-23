from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from SGCAS.decorators import requiere_permiso
from apps.fase.models import Fase
from apps.item.models import Item
from apps.linea_base.forms import LineaBaseForm, AgregarItemsForm, LineaBaseUpdateEstado
from apps.linea_base.models import LineaBase

"""
Todas las vistas para la aplicación del Modulo Línea Base
Actualmente se despliega en las plantillas 7 vistas:

1. **crear_linea_base** - crea la línea base (Ir a la sección: [[views.py #crear línea base]] )
2. **agregar_items_lb** - agrega ítems aprobados a la línea base (Ir a la sección: [[views.py #agregar ítems lb]] )
3. **editar_lb** - modifica los atributos de la línea base (Ir a la sección: [[views.py #editar lb]] )
4. **estado_lb** - modifica el estado de una línea base (Ir a la sección: [[views.py #estado lb]] )
5. **lista_linea_base** - lista las líneas base de una fase (Ir a la sección: [[views.py #lista de líneas base]] )
6. **search** - despliega las líneas base buscadas de una fase (Ir a la sección: [[views.py #search]] )
7. **lista_items_linea_base** - lista todos los ítems que forman parte de una línea base (Ir a la sección: [[views.py #lista ítems lb]] )
"""


@requiere_permiso('crear_linea_base')
# === crear línea base ===
def crear_linea_base(request, id_fase):
    """
    Permite la creación de una instancia de objeto línea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de la instancia de fase en donde se esta creando la línea base.<br/>
    **:return:** Retorna una instancia de línea base creada.<br/>
    """
    # query_item = Item.objects.all().filter(fase_id=id_fase)
    # flag = False
    fase = Fase.objects.get(id=id_fase)
    # for item in query_item:
    #     if item.estado == "Aprobado" and item.padres.all().exists() and item.hijos.all().exists() and item.antecesores.all().exists() and item.sucesores.all().exists():
    #         flag = True
    cant_items_sueltos = cant_item_libres(fase)
    if request.method == 'POST':
        form = LineaBaseForm(request.POST)
        if form.is_valid():
            lb = form.save(commit=False)
            lb.fase = Fase.objects.get(id=id_fase)
            lb.save()
            return redirect('linea_base:agregar_items_lb', pk=lb.pk, id_fase=id_fase)
    # elif flag and fase.proyecto.estado == "Iniciado":
    elif fase.proyecto.estado == "Iniciado":
        form = LineaBaseForm()
        return render(request, 'linea_base/linea_crear.html', {'form': form, 'cant_items_sueltos':cant_items_sueltos})
    else:
        # return render(request, 'linea_base/linea_crear.html', {'flag': flag, 'fase': fase})
        return render(request, 'linea_base/linea_crear.html', {'fase': fase, 'cant_items_sueltos':cant_items_sueltos})


def cant_item_libres(fase):
    """
    Permite conocer la cantidad de items libres en una fase.<br/>
    **:param fase:** Recibe la instancia de fase sobre el cual se desea se desea operar.<br/>
    **:return:** Retorna un numero entero que es la cantidad de items libres en la fase.<br/>
    """
    items_en_lb = 0
    for lb in LineaBase.objects.filter(fase=fase):
        if lb.estado != 'Rota':
            items_en_lb += lb.items.all().count()
    return items_en_lb-Item.objects.filter(fase=fase).count()


@requiere_permiso('agregar_item_linea_base')
# === agregar ítems lb ===
def agregar_items_lb(request, pk, id_fase):
    """
    Permite agregar ítems a una línea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de línea base, en donde se asignaran los ítems.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la línea base.<br/>
    **:return:** Retorna una línea base con sus ítems agregados.<br/>
    """
    form = AgregarItemsForm(request.POST or None, instance=get_object_or_404(LineaBase, pk=pk), id_fase=id_fase)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('linea_base:linea_lista', id_fase=id_fase)
    else:
        items_aprobados = Item.objects.filter(fase=id_fase).filter(estado='Aprobado')
        return render(request, 'linea_base/linea_agregar_items.html', {'form': form,
                                                                       'fase': Fase.objects.get(id=id_fase),
                                                                       'items_aprobados': items_aprobados})


@requiere_permiso('editar_linea_base')
# === editar lb ===
def editar_lb(request, pk, id_fase):
    """
      Permite la modificación de una instancia de línea base.<br/>
      **:param request:** Recibe un request por parte de un usuario.<br/>
      **:param pk:** Recibe pk de una instancia de línea base que se desea modificar.<br/>
      **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la línea base.<br/>
      **:return:** Retorna una línea base modificada.<br/>
      """
    form = LineaBaseForm(request.POST or None, instance=get_object_or_404(LineaBase, pk=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('linea_base:linea_lista', id_fase=id_fase)
    else:
        return render(request, 'linea_base/linea_crear.html', {'form': form})


@requiere_permiso('estado_linea_base')
# === estado lb ===
def estado_lb(request, pk, id_fase):
    """
    Permite la modificación de una línea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de línea base, la que cambiará de estado.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la línea base.<br/>
    **:return:** Retorna una línea base con su estado modificado.<br/>
    """
    lb = get_object_or_404(LineaBase, pk=pk)
    form = LineaBaseUpdateEstado(request.POST or None, instance=lb)
    if form.is_valid():
        form.save()
        return redirect('linea_base:linea_lista', id_fase=id_fase)
    return render(request, 'linea_base/linea_base_estado.html', {'form': form})


@requiere_permiso('listar_linea_base')
# === lista de líneas base ===
def lista_linea_base(request, id_fase):
    """
    Permite visualizar la lista de líneas bases de una fase en particular.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, de la cual requerimos la lista de líneas bases.<br/>
    **:return:** Retorna una lista de líneas bases.<br/>
    """
    lista_lb = LineaBase.objects.filter(fase=Fase.objects.get(id=id_fase)).order_by('id').distinct()
    paginator = Paginator(lista_lb, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'linea_base/linea_lista.html',
                  {'lb': LineaBase.objects.filter(fase=Fase.objects.get(id=id_fase)),
                   'fase': Fase.objects.get(id=id_fase), 'page_obj': page_obj})


@requiere_permiso('listar_linea_base')
# === search ===
def search(request, id_fase):
    """
    Permite realizar la búsqueda de líneas bases de una fase en particular.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, de la cual requerimos la lista de líneas bases.<br/>
    **:return:** Retorna una lista de líneas bases que satifacen el criterio de búsqueda.<br/>
    """
    template = 'linea_base/list_busqueda.html'
    query = request.GET.get('buscar')

    fase = Fase.objects.get(id=id_fase)

    if query:
        results = LineaBase.objects.filter(Q(fase=Fase.objects.get(id=id_fase)) &
                                           (Q(identificador__icontains=query) | Q(
                                               descripcion__contains=query))).order_by('id').distinct()
    else:
        results = LineaBase.objects.filter(Q(fase=Fase.objects.get(id=id_fase))).order_by('id').distinct()

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'lb': results,
        'fase': fase,
        'page_obj': page_obj
    }
    return render(request, template, context)


@requiere_permiso('listar_item_linea_base')
# === lista ítems lb ===
def lista_items_linea_base(request, pk, id_fase):
    """
    Permite visualizar la lista de ítems correspondientes a una línea base en particular.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de línea base, de la cual requerimos la lista de ítems.<br/>
    **:param id_fases:** Recibe el id de la fase a la que pertenece, para regresar a la lista de líneas base.<br/>
    **:return:** Retorna una lista de ítems correspondientes a una línea base.<br/>
    """
    lista_item_lb = get_object_or_404(LineaBase, pk=pk).items.all().order_by('id').distinct()
    fase = Fase.objects.get(id=id_fase)

    paginator = Paginator(lista_item_lb, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'linea_base/linea_items_lista.html',
                  {'items': lista_item_lb, 'page_obj': page_obj, 'fase': fase})


@requiere_permiso('eliminar_linea_base')
def eliminar_lb(request, pk, id_fase):
    """
    Permite la eliminacion de una instancia de linea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de linea base,que se eliminara<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la linea base.<br/>
    **:return:** Retorna una instancia de linea base eliminada.<br/>
    """
    get_object_or_404(LineaBase, pk=pk).delete()
    return redirect('linea_base:linea_lista', id_fase=id_fase)

# **Volver atras** : [[urls.py]]

# === Indice de la documentación de la Aplicación linea base  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
