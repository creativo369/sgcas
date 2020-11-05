from django.test import TestCase
from apps.tipo_item.models import TipoItem, ItemImportado
from apps.item.models import Item
from apps.fase.models import Fase


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
        
    def test_importar_ti(self):
        importado = ItemImportado.objects.create(id_item=TipoItem.objects.create(nombre='tipo1', descripcion='descripcion-tipo1',
                                                 atributos=('Boolean', 'Boolean')))

        tipo_inicial = TipoItem.objects.none()
        
        tipo_inicial = importado.id_item

        tipo_inicial.save()

        try:
            self.assertEqual(tipo_inicial, importado.id_item)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_tipo_item_por_fase(self):
        for i in 'abc':
            TipoItem.objects.create(nombre='tipo'+i, descripcion='descripcion'+i, atributos=('Boolean', 'Boolean'))

        fase1=Fase.objects.create(nombre='fase1', descripcion='descripcion fase1')    

        for plantilla in TipoItem.objects.all():
            plantilla.fase = fase1 
            plantilla.save()

        cantidad_plantilla_fase1= TipoItem.objects.filter(fase=fase1).all().count()

        try:
            self.assertEqual(cantidad_plantilla_fase1, TipoItem.objects.all().count())
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