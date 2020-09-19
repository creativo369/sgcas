from django.test import TestCase
from apps.fase.models import Fase
from apps.proyecto.models import Proyecto

class TestFaseSetUp(TestCase):
    def setUp(self):
        self.nombre = 'fase-prueba'
        self.descripcion = 'descripcion-fase-prueba'
        self.estado = 'Abierta'
        self.proyecto = Proyecto.objects.first()

class FaseTestCrear(TestFaseSetUp):

    def setUp(self):
        super(FaseTestCrear, self).setUp()

    def test_nombre(self):
        try:    
            self.assertEqual(self.nombre, 'fase-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_descripcion(self):
        try:    
            self.assertEqual(self.descripcion, 'descripcion-fase-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        
       

    def test_pertenece_proyecto(self):
        try:    
            self.assertEqual(self.proyecto, Proyecto.objects.first())
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        
 
        

   
class FaseTestEditar(TestFaseSetUp):

    def setUp(self):
        super(FaseTestEditar, self).setUp()

    def test_editar_nombre(self):
        nombre_anterior = self.nombre
        self.nombre = 'fase-test-nombre-cambiado'
        try:    
            self.assertNotEqual(self.nombre, nombre_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        


    def test_editar_descripcion(self):
        descripcion_anterior = self.descripcion
        self.descripcion = 'descripcion-cambiada-test' 
        try:    
            self.assertNotEqual(self.descripcion, descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        
        


# **Volver atras** : [[forms.py]]

# **Ir a la documentación de urls de la fase** : [[urls.py]]

# === Indice de la documentación de la Aplicación fase  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)