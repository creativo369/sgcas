from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.proyecto.models import Proyecto
from apps.fase.models import Fase

class TestLBSetUp(TestCase):
    def setUp(self):
        self.descripcion = 'descripcion_LB'        
        self.fase = Fase.objects.create(nombre='fase_test', descripcion='fase_test',
        		proyecto=Proyecto.objects.first())
        
class LBTestCrear(TestLBSetUp):

    def setUp(self):
        super(LBTestCrear, self).setUp()

    def test_descripcion(self):
        descripcion_lb = 'descripcion_LB'
        
        if not self.descripcion == descripcion_lb:
            raise ValidationError('Datos proporcionados no coinciden')
  

    def test_pertenece_fase(self):
        fase = Fase.objects.none()
        fase = Fase.objects.first()
        
        if not self.fase == fase:
            raise ValidationError ('Datos proporcionados no coinciden')


class LBTestEditar(TestLBSetUp):

    def setUp(self):
        super(LBTestEditar, self).setUp()        

    def test_editar_descripcion(self):
        descripcion_anterior = self.descripcion
        self.descripcion = 'lb-test-descripcion-cambiada'        
        
        if self.descripcion == descripcion_anterior:
            raise ValidationError('Datos proporcionados son iguales.')


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