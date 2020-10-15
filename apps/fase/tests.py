from django.test import TestCase
from apps.fase.models import Fase
from django.contrib.auth.models import Group
from apps.proyecto.models import Proyecto
from apps.usuario.models import User
from apps.item.models import Item
from apps.tipo_item.models import TipoItem
from apps.rol.models import Rol

class TestFaseSetUp(TestCase):
    def setUp(self):
        self.fase = Fase.objects.create(nombre='fase-prueba', descripcion = 'descripcion-fase-prueba',
                                        estado = 'Abierta', proyecto = Proyecto.objects.first())
        self.fase.miembros.add(User.objects.create(username='Pepe'))


class FaseTestCrear(TestFaseSetUp):

    def setUp(self):
        super(FaseTestCrear, self).setUp()

    def test_nombre(self):
        try:    
            self.assertEqual(self.fase.nombre, 'fase-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_descripcion(self):
        try:    
            self.assertEqual(self.fase.descripcion, 'descripcion-fase-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        
       

    def test_pertenece_proyecto(self):
        try:    
            self.assertEqual(self.fase.proyecto, Proyecto.objects.first())
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        
 
        

   
class FaseTestEditar(TestFaseSetUp):

    def setUp(self):
        super(FaseTestEditar, self).setUp()

    def test_editar_nombre(self):
        nombre_anterior = self.fase.nombre
        self.fase.nombre = 'fase-test-nombre-cambiado'
        try:    
            self.assertNotEqual(self.fase.nombre, nombre_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        


    def test_editar_descripcion(self):
        descripcion_anterior = self.fase.descripcion
        self.fase.descripcion = 'descripcion-cambiada-test' 
        try:    
            self.assertNotEqual(self.fase.descripcion, descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
            

    def test_agregar_y_quitar_miembros_fase(self):
        #agregando miembros
        for m in 'abc':
          self.fase.miembros.add(User.objects.create(username='r'+ m))        
        try:
            self.assertEqual(len(self.fase.miembros.all()),4)
        except AssertionError as e:        
             print("Error de comparacion: {}".format(e))


        #eliminando el ultimo miembro de la fase 
        cant_miembros= len(self.fase.miembros.all())       

        try:
            self.assertNotEqual(len(self.fase.miembros.last().delete()),cant_miembros)
        except AssertionError as e:        
             print("Error de comparacion: {}".format(e))

    def test_agregar_item_fase(self):
        cant_item_de_fase = len(Item.objects.filter(fase=self.fase)) #inicialmente hay cero ítems

        for i in 'abc':
            Item.objects.create(nombre='item '+i, descripcion='decripcion '+i, costo=5, fase= self.fase)

        try:
            self.assertNotEqual(len(Item.objects.filter(fase=self.fase)),cant_item_de_fase)
        except AssertionError as e:        
             print("Error de comparacion: {}".format(e))

    def test_agregar_tipo_item_fase(self):
        cant_tipo_item_de_fase = len(TipoItem.objects.filter(fase=self.fase)) #inicialmente hay cero tipos de ítem

        for i in 'abc':
            TipoItem.objects.create(nombre='tipo-item-test ' + i, descripcion='descripcion-test',
                                                 atributos=('Boolean', 'Boolean'), fase= self.fase)

        try:
            self.assertNotEqual(len(TipoItem.objects.filter(fase=self.fase)),cant_tipo_item_de_fase)
        except AssertionError as e:        
             print("Error de comparacion: {}".format(e))

    def test_agregar_rol_fase(self):
        cant_rol_de_fase = len(Rol.objects.filter(fase=self.fase)) #inicialmente hay cero roles

        for i in 'abc':
            Rol.objects.create(nombre='rol '+ i, group= Group.objects.create(name='grupo-fase '+i), fase= self.fase)

        try:
            self.assertNotEqual(len(Rol.objects.filter(fase=self.fase)), cant_rol_de_fase)
        except AssertionError as e:        
             print("Error de comparacion: {}".format(e))         

class FaseTestEliminar(TestFaseSetUp):
    def setUp(self):
        super(FaseTestEliminar, self).setUp()
        self.id_fase = self.fase.id

    def __del__(self):
        pass        

    def test_eliminar_fase(self):
        self.fase.delete()
        
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