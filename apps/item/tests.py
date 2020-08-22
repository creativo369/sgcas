from datetime import datetime

from apps.usuario.models import User
from django.test import TestCase
from apps.item.models import Item


class ItemSetUpTest(TestCase):
    def setUp(self):
        self.usarios_a_cargo = User.objects.create(username='user-a-cargo-item')
        self.item = Item.objects.create(nombre='item-test', descripcion='descripcion-test', estado='Desarrollo',
                                        costo=2)
        self.item.usuarios_a_cargo.add(self.usarios_a_cargo)

    def test_crear_item(self):
        nombre_item = self.item.nombre
        self.assertEqual(self.item.nombre, nombre_item)
        print('Item-test_crear_item OK')

    def test_modificar_item(self):
        descripcion_pasada = self.item.descripcion
        self.item.descripcion = 'Nueva descripcion'
        self.assertNotEqual(self.item.descripcion, descripcion_pasada)
        print('Item-test_modificar_item OK')

    def test_eliminar_item(self):
        self.item.delete()

    def __del__(self):
        print('Item-test_eliminar_item OK')

# **Volver atras** : [[models.py]]

# **Ir a la documentación de URLS del modulo item** : [[urls.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
