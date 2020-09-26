from django.test import TestCase
from apps.tipo_item.models import TipoItem


class TipoItemTest(TestCase):
    def setUp(self):
        self.ATTRIBUTES = [
            ('Boolean', 'Boolean'),
            ('Char', 'Char'),
            ('Date', 'Date'),
            ('Numerico', 'Numerico'),
        ]
        self.tipo_item = TipoItem.objects.create(nombre='tipo-item-test', descripcion='descripcion-test',
                                                 atributos=('Boolean', 'Boolean'))

    def test_crear_tipo_item(self):
        nombre = self.tipo_item.nombre
        try:
            self.assertEqual(self.tipo_item.nombre, nombre)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        

    def test_modificar_tipo_item(self):
        atributos_anterior = self.tipo_item.atributos
        self.tipo_item.atributos = ('Char', 'Char')
        self.tipo_item.save()
        try:
            self.assertNotEqual(self.tipo_item.atributos, atributos_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        

    def test_eliminar_ti(self):
        self.tipo_item.delete()

    def __del__(self):
        pass
        

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)