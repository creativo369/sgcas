from django.shortcuts import render, redirect
from apps.tipo_item.forms import TipoItemForm
from apps.tipo_item.models import TipoItem
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def crear_tipo_item(request):
	if request.method == 'POST':
		form = TipoItemForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('tipo_item:tipo_item_opciones')
	else:
		form = TipoItemForm()

	return render(request, 'tipo_item/tipo_item_crear.html', {'form':form})

def tipo_item_opciones(request):
	return render(request, 'tipo_item/tipo_item_opciones.html')


class TipoItemLista(ListView):
	model = TipoItem
	template_name = 'tipo_item/tipo_item_lista.html'

class TipoItemEliminar(DeleteView):
	model = TipoItem
	template_name = 'tipo_item/tipo_item_eliminar.html'
	# permission_required = 'auth.delete_user'
	success_url = reverse_lazy('tipo_item:tipo_item_lista')