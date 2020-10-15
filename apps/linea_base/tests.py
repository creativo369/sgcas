from django.test import TestCase
from apps.proyecto.models import Proyecto
from apps.fase.models import Fase
from apps.item.models import Item
from apps.linea_base.models import LineaBase

class TestLBSetUp(TestCase):
    def setUp(self):
        self.linea_base = LineaBase.objects.create(descripcion='descripcion_LB')
        self.linea_base.fase = Fase.objects.create(nombre='fase_test', descripcion='fase_test',
                proyecto=Proyecto.objects.first())
        self.linea_base.items.add(Item.objects.create(nombre='Item1', estado='Aprobado', descripcion= 'descripcion Item1',costo=8))

class LBTestCrear(TestLBSetUp):

    def setUp(self):
        super(LBTestCrear, self).setUp()

    def test_descripcion(self):
        descripcion_lb = 'descripcion_LB'
        try:        
            self.assertEqual(self.linea_base.descripcion, descripcion_lb)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
  

    def test_pertenece_fase(self):
        try:        
            self.assertEqual(self.linea_base.fase, Fase.objects.first())
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_item(self):
        nombre_item = 'Item1'
        try:        
            self.assertEqual(self.linea_base.items.first().nombre, nombre_item)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
          




class LBTestEditar(TestLBSetUp):

    def setUp(self):
        super(LBTestEditar, self).setUp()        

    def test_editar_descripcion(self):
        descripcion_anterior = self.linea_base.descripcion
        self.linea_base.descripcion = 'lb-test-descripcion-cambiada'        
        try:        
            self.assertNotEqual(self.linea_base.descripcion, descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        

    def test_editar_item(self):
        nombre_item_anterior = self.linea_base.items.first().nombre
        self.linea_base.items.all().update(nombre = 'Item2')
            
        try:        
            self.assertNotEqual(self.linea_base.items.first().nombre, nombre_item_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        
    def test_agregar_y_quitar_items(self):        
        #Agregar ítems
        for r in 'abc':
            self.linea_base.items.add(Item.objects.create(nombre='Item1'+r, descripcion= 'descripcion Item1'+r,
                estado='Aprobado',costo=8))

        try:        
            self.assertEqual(len(self.linea_base.items.all()),4)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

        #Quitar ítems
        cantidad_ítems=len(self.linea_base.items.all())

        try:        
            self.assertNotEqual(len(self.linea_base.items.first().delete()), cantidad_ítems)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_cerrar_linea_base(self):
        #se cargan los items aprobados a la LB para la prueba
        for a in 'abc':
            self.linea_base.items.add(Item.objects.create(nombre='Item '+ a, descripcion='descripcion ' + a,
                                                    costo=17, estado= 'Aprobado' ))

        no_aprobados = 0
        anterior_estado= self.linea_base.estado

        for item in self.linea_base.items.all():
            if not item.estado == 'Aprobado':
                no_aprobados = 1    #verifica si todos los ítems de la LB están aprobados

        if no_aprobados==0:
            self.linea_base.estado= 'Cerrada'

        try:        
            self.assertNotEqual(anterior_estado, self.linea_base.estado)
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