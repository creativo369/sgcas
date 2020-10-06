# ESCENARIO 1 : Proyecto creado sin iniciar

"""
    Escenario 1 implica:
        0.Crear un rol de sistema y asignar a usuarios creados.
        1.Crear el proyecto :nombre, descripcion, agregar miembros.
        2.Crear comite :nombre del comite, descripcion, miembros.
        3.Crear al menos 3 fases :nombre de la fase, descripción y miembros.
        4.Crear roles por fases y asignar a los miembros de las fases.

"""

import os
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGCAS.settings.desarrollo")
django.setup()

from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from apps.usuario.models import User
from apps.proyecto.models import Proyecto
from apps.comite.models import Comite
from apps.rol.models import Rol
from apps.fase.models import Fase

# Filtramos los permisos de sistema del core de django
permisos_sistema = Permission.objects.filter(
    Q(codename='crear_rol_sistema')
    | Q(codename='editar_rol_sistema')
    | Q(codename='gestion_rol_sistema')
    | Q(codename='listar_rol_sistema')
    | Q(codename='eliminar_rol_sistema')
    | Q(codename='asignar_rol_sistema')
    | Q(codename='registrar_usuario')
    | Q(codename='editar_usuario')
    | Q(codename='eliminar_usuario')
    | Q(codename='ver_usuario')
    | Q(codename='gestion_usuario')
    | Q(codename='ver_mensaje')
    | Q(codename='mensaje_editar')
    | Q(codename='mensaje_rechazar')
    | Q(codename='crear_proyecto')
    | Q(codename='editar_proyecto')
    | Q(codename='ver_proyecto')
    | Q(codename='gestion_proyecto')
    | Q(codename='eliminar_proyecto')
    | Q(codename='cambiar_estado')
    | Q(codename='detalles_proyecto')
    | Q(codename='crear_comite')
    | Q(codename='editar_comite')
    | Q(codename='ver_comite')
    | Q(codename='eliminar_comite')
    | Q(codename='crear_fase')
    | Q(codename='listar_fase')
    | Q(codename='gestion_fase')
    # === Permisos para roles por fase
    | Q(codename='crear_rol')
    | Q(codename='listar_rol')
    | Q(codename='asignar_rol')
    | Q(codename='editar_rol')
    | Q(codename='eliminar_rol')
)
# # creamos un grupo rol_sistema
rol_sistema = Group.objects.create(
    name="Rol de Sistema 1"
)
# # Agregamos todos los permisos del sistema a un rol de sistema
for permiso in permisos_sistema:
    rol_sistema.permissions.add(permiso)
    rol_sistema.save()
# Creamos 6 usuarios para poblar la base de datos y para las pruebas pertinentes
for x in range(6):
    usuario = User.objects.create(
        username='Usuario' + str(x)
    )
    usuario.save()

# El gerente es el administrador
query_admin = User.objects.filter(is_superuser=True)
# Creamos el proyecto
proyecto_escena1 = Proyecto.objects.create(
    nombre="Proyecto Escenario 1",
    descripcion="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    gerente_id=query_admin[0].id  # extraemos de la lista al primer admin de django
)

# Colocamos los usuarios a activos y le asignamos un rol de sistema
# Asignamos los usuarios al proyecto
for usuario in User.objects.all().exclude(username='AnonymousUser'):
    usuario.is_active = True
    usuario.groups.add(rol_sistema)
    proyecto_escena1.miembros.add(usuario)
    usuario.save()
    proyecto_escena1.save()

comite_escena1 = Comite.objects.create(
    nombre="Comite Escenario 1",
    descripcion="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    proyecto_id=proyecto_escena1.id
)
for usuario in User.objects.all().exclude(username='AnonymousUser'):
    comite_escena1.miembros.add(usuario)
    comite_escena1.save()

for x in range(3):
    fase_proyecto = Fase.objects.create(
        nombre="Fase" + str(x),
        descripcion="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        proyecto_id=proyecto_escena1.id
    )
    fase_proyecto.save()

for fase in Fase.objects.filter(proyecto_id=proyecto_escena1.id):
    for miembro_fase in User.objects.all().exclude(username='AnonymousUser'):
        fase.miembros.add(miembro_fase)
        fase.save()

permisos_rol_fase = Permission.objects.filter(
    Q(codename='editar_fase')
    | Q(codename='detalles_fase')
    | Q(codename='eliminar_fase')
    | Q(codename='cambio_estado_fase')
    | Q(codename='crear_item')
    | Q(codename='editar_item')
    | Q(codename='listar_item')
    | Q(codename='ver_item')
    | Q(codename='eliminar_item')
    | Q(codename='cambiar_estado_item')
    | Q(codename='relacion_item')
    | Q(codename='calcular_impacto')
    | Q(codename='ver_trazabilidad')
    | Q(codename='versiones_item')
    | Q(codename='restaurar_item_version')
    | Q(codename='item_modificar_atributos')
    | Q(codename='item_modificar_ti')
    | Q(codename='item_modificar_atributos_ti')
    | Q(codename='item_modificar_import_ti')
    | Q(codename='crear_tipo_item')
    | Q(codename='editar_tipo_item')
    | Q(codename='listar_tipo_item')
    | Q(codename='ver_tipo_item')
    | Q(codename='eliminar_tipo_item')
    | Q(codename='adjuntar_tipo_item')
    | Q(codename='importar_tipo_item')
    | Q(codename='crear_linea_base')
    | Q(codename='editar_linea_base')
    | Q(codename='eliminar_linea_base')
    | Q(codename='listar_linea_base')
    | Q(codename='estado_linea_base')
    | Q(codename='agregar_item_linea_base')
    | Q(codename='quitar_item_linea_base')
    | Q(codename='listar_item_linea_base')
)

grupo_rol_fase = Group.objects.create(
    name='Rol de Fase'
)

# # Agregamos todos los permisos que puedan haber en un rol por fase
for permiso in permisos_rol_fase:
    grupo_rol_fase.permissions.add(permiso)
    grupo_rol_fase.save()

# # creamos un grupo rol_fase
fase_p = Fase.objects.all().filter(proyecto=proyecto_escena1.id)
rol_fase = Rol.objects.create(
    nombre="Rol de Fase " + str(0),
    group=grupo_rol_fase,
    fase=fase_p[0]
)
rol_fase.save()

fase = Fase.objects.all().filter(proyecto=proyecto_escena1.id)

for usuario_miembro in fase[0].miembros.all():
    rol_fase.usuarios.add(usuario_miembro)
    rol_fase.save()

if __name__ == "__main__":
    print("Inicio de creación de población de base de datos del script <<< Escenario 1 >>>")
    print("Por favor espere . . . ")
    start = time.strftime("%c")
    print(f'Fecha y hora de inicio: {start}')
    end = time.strftime("%c")
    print(f'Fecha y hora de finalización: {end}')
