from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from apps.fase.models import Fase
from apps.item.models import Item
from apps.linea_base.forms import LineaBaseForm, AgregarItemsForm, LineaBaseUpdateEstado
from apps.linea_base.models import LineaBase


def crear_linea_base(request, id_fase):
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


def agregar_items_lb(request, pk, id_fase):
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


def editar_lb(request, pk, id_fase):
    form = LineaBaseForm(request.POST or None, instance=get_object_or_404(LineaBase, pk=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('linea_base:linea_lista', id_fase=id_fase)
    else:
        return render(request, 'linea_base/linea_crear.html', {'form': form})


def estado_lb(request, pk, id_fase):
    lb = get_object_or_404(LineaBase, pk=pk)
    form = LineaBaseUpdateEstado(request.POST or None, instance=lb)
    if form.is_valid():
        form.save()
        return redirect('linea_base:linea_lista', id_fase=id_fase)
    return render(request, 'linea_base/linea_base_estado.html', {'form': form})


def lista_linea_base(request, id_fase):
    return render(request, 'linea_base/linea_lista.html',
                  {'lb': LineaBase.objects.filter(fase=Fase.objects.get(id=id_fase)),
                   'fase': Fase.objects.get(id=id_fase)})


def lista_items_linea_base(request, pk):
    return render(request, 'linea_base/linea_items_lista.html',
                  {'items': get_object_or_404(LineaBase, pk=pk).items.all()})


def eliminar_lb(request, pk, id_fase):
    get_object_or_404(LineaBase, pk=pk).delete()
    return redirect('linea_base:linea_lista', id_fase=id_fase)
