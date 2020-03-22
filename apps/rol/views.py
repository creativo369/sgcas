from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from apps.rol.forms import GroupForm
from django.shortcuts import render, redirect

@login_required
@permission_required('auth.add_group')
def crear_rol_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('rol:rol_lista')
    else:
        form = GroupForm()
    return render(request,'rol/rol_crear.html', {'form': form})


def rol_opciones(request):
	return render(request, 'rol/rol_opciones.html')

class ListaRol(PermissionRequiredMixin, ListView):
	model = Group
	template_name = 'rol/rol_lista.html'
	permission_required = 'auth.change_group'

class EditarRol(PermissionRequiredMixin,UpdateView):
    model = Group
    form_class = GroupForm
    permission_required = 'auth.change_group'
    template_name = 'rol/rol_editar.html'
    success_url = reverse_lazy('rol:rol_lista')

class EliminarRol(PermissionRequiredMixin, DeleteView):
	model = Group
	template_name = 'rol/rol_eliminar.html'
	permission_required = 'auth.delete_group'
	success_url = reverse_lazy('rol:rol_lista')

