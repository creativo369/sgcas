from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404

from apps.fase.models import Fase
from apps.item.models import Item
from apps.linea_base.forms import LineaBaseForm, AgregarItemsForm, LineaBaseUpdateEstado
from apps.linea_base.models import LineaBase


@permission_required('linea_base.crear_linea_base')
def crear_linea_base(request, id_fase):
    """
    Permite la creacion de una instancia de objeto linea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de la instancia de fase en donde se esta creando la linea base<br/>
    **:return:** Retorna una instancia de linea base creada,<br/>
    """
    if request.method == 'POST':
        form = LineaBaseForm(request.POST)
        if form.is_valid():
            lb = form.save(commit=False)
            lb.fase = Fase.objects.get(id=id_fase)
            lb.save()
            return redirect('linea_base:agregar_items_lb', pk=lb.pk, id_fase=id_fase)
    else:
        form = LineaBaseForm()
        return render(request, 'linea_base/linea_crear.html', {'form': form})


@permission_required('linea_base.agregar_item_linea_base')
def agregar_items_lb(request, pk, id_fase):
    """
    Permite agregar items a una linea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de linea base, en donde se asignaran los items.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la linea base.<br/>
    **:return:** Retorna una linea base con sus items agregados.<br/>
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


@permission_required('linea_base.editar_linea_base')
def editar_lb(request, pk, id_fase):
    """
      Permite la modificacion de una instancia de linea base.<br/>
      **:param request:** Recibe un request por parte de un usuario.<br/>
      **:param pk:** Recibe pk de una instancia de linea base que se desea modificar.<br/>
      **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la linea base.<br/>
      **:return:** Retorna una linea base modificada.<br/>
      """
    form = LineaBaseForm(request.POST or None, instance=get_object_or_404(LineaBase, pk=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('linea_base:linea_lista', id_fase=id_fase)
    else:
        return render(request, 'linea_base/linea_crear.html', {'form': form})


@permission_required('linea_base.editar_linea_base')
def estado_lb(request, pk, id_fase):
    """
    Permite la modificacion de una linea base.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de linea base, la que cambiara de estado.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, en donde se encuentra la linea base.<br/>
    **:return:** Retorna una linea base con su estado modificado.<br/>
    """
    lb = get_object_or_404(LineaBase, pk=pk)
    form = LineaBaseUpdateEstado(request.POST or None, instance=lb)
    if form.is_valid():
        form.save()
        return redirect('linea_base:linea_lista', id_fase=id_fase)
    return render(request, 'linea_base/linea_base_estado.html', {'form': form})


@permission_required('linea_base.ver_linea_base')
def lista_linea_base(request, id_fase):
    """
    Permite visualizar la lista de lineas bases de una fase en particular.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe pk de una instancia de fase, de la cual requerimos la lista de lineas bases.<br/>
    **:return:** Retorna una lista de lineas bases.<br/>
    """
    return render(request, 'linea_base/linea_lista.html',
                  {'lb': LineaBase.objects.filter(fase=Fase.objects.get(id=id_fase)),
                   'fase': Fase.objects.get(id=id_fase)})


@permission_required('linea_base.listar_item_linea_base')
def lista_items_linea_base(request, pk):
    """
    Permite visualizar la lista de items correspondientes a una linea base en particular.<br/>
    **:param request:**Recibe un request por parte de un usuario.<br/>
    **:param pk:** Recibe pk de una instancia de linea base, de la cual requerimos la lista de items.<br/>
    **:return:** Retorna una lista de items correspondientes a una linea base.<br/>
    """
    return render(request, 'linea_base/linea_items_lista.html',
                  {'items': get_object_or_404(LineaBase, pk=pk).items.all()})


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
