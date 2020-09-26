from django.test import TestCase
from apps.proyecto.models import Proyecto
from apps.fase.models import Fase
from apps.item.models import Item

class TestLBSetUp(TestCase):
    def setUp(self):
        self.descripcion = 'descripcion_LB'        
        self.fase = Fase.objects.create(nombre='fase_test', descripcion='fase_test',
        		proyecto=Proyecto.objects.first())
        self.items = Item.objects.none()

class LBTestCrear(TestLBSetUp):

    def setUp(self):
        super(LBTestCrear, self).setUp()

    def test_descripcion(self):
        descripcion_lb = 'descripcion_LB'
        try:        
            self.assertEqual(self.descripcion, descripcion_lb)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
  

    def test_pertenece_fase(self):
        try:        
            self.assertEqual(self.fase, Fase.objects.first())
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
          




class LBTestEditar(TestLBSetUp):

    def setUp(self):
        super(LBTestEditar, self).setUp()        

    def test_editar_descripcion(self):
        descripcion_anterior = self.descripcion
        self.descripcion = 'lb-test-descripcion-cambiada'        
        try:        
            self.assertNotEqual(self.descripcion,descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        

    def test_editar_item(self):
        item_anterior = self.items
        self.items = Item.objects.create(nombre= 'Item1', descripcion='descripcion item 1', costo=6)        
        try:        
            self.assertNotEqual(self.items,item_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        



# **Volver atras** : [[apps.py]]

# **Ir a la documentación del URL de linea base** : [[urls.py]]

# === Indice de la documentación de la Aplicación linea base  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)