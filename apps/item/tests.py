from datetime import datetime
from apps.usuario.models import User
from django.test import TestCase
from apps.item.models import Item
from apps.tipo_item.models import TipoItem


class ItemSetUpTest(TestCase):
    def setUp(self):
        self.usarios_a_cargo = User.objects.create(username='user-a-cargo-item')
        self.item = Item.objects.create(nombre='item-test', descripcion='descripcion-test', estado='Desarrollo',
                                        costo=2)
        self.item.usuarios_a_cargo.add(self.usarios_a_cargo)
        self.tipo_item = TipoItem.objects.create(nombre='tipo1', descripcion='descripcion-tipo1',
                                                 atributos=('Boolean', 'Boolean'))

        self.padres = Item.objects.create(nombre='Item', descripcion='descripcion item', costo=3)

    def test_crear_item(self):
        nombre_item = self.item.nombre
        try:
            self.assertEqual(self.item.nombre, nombre_item)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_modificar_item(self):
        descripcion_pasada = self.item.descripcion
        self.item.descripcion = 'Nueva descripcion'
        try:
            self.assertNotEqual(self.item.descripcion, descripcion_pasada)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_modificar_padres_y_TI(self):
        anterior_TI = TipoItem.objects.none()
        anterior_TI = self.tipo_item
        self.tipo_item = TipoItem.objects.create(nombre='tipo1', descripcion='descripcion-tipo1',
                                                 atributos=('Char', 'Char'))

        try:
            self.assertNotEqual(self.tipo_item, anterior_TI)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

        anterior_padres = Item.objects.none()
        anterior_padres = self.padres
        self.padres = Item.objects.create(nombre='Item1', descripcion='descripcion item 1', costo=5)

        try:
            self.assertNotEqual(self.padres, anterior_padres)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_eliminar_item(self):
        self.item.delete()

    def __del__(self):
        pass

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

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
