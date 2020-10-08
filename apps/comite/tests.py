from apps.usuario.models import User
from django.test import TestCase
from apps.comite.models import Comite
from apps.proyecto.models import Proyecto

class TestComiteSetUp(TestCase):
    def setUp(self):
        self.proyecto = Proyecto.objects.first()
        self.miembro = User.objects.create(username='miembro-comite-test')
        self.comite = Comite.objects.create(nombre='comite-test', descripcion='descripcion-comite-test',
                                            proyecto=self.proyecto)
        self.comite.miembros.add(self.miembro)


class ComiteTestCrear(TestComiteSetUp):

    def setUp(self):
        super(ComiteTestCrear, self).setUp()

    def test_nombre(self):
        try:    
            self.assertEqual(self.comite.nombre, 'comite-test')
        except AssertionError  as e:
            print("Error de comparacion: {}".format(e))

    def test_agregar_miembros(self):
        for r in 'ab':
          self.comite.miembros.add(User.objects.create(username='a'+ r))
        try:
            self.assertEqual(len(self.comite.miembros.all()),3)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))


    def test_descripcion(self):
        try:
            self.assertEqual(self.comite.descripcion, 'descripcion-comite-test')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        
        

    def test_pertenece_proyecto(self):
        try:
            self.assertEqual(self.comite.proyecto, self.proyecto)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e)) 
        


    def test_miembro(self):
        try:
            self.assertEqual(self.comite.miembros.first(), self.miembro)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))
        

        


class ComiteTestEditar(TestComiteSetUp):

    def setUp(self):
        super(ComiteTestEditar, self).setUp()
        self.miembro_2 = User.objects.create(username='miembro-comite-2')

    def test_editar_nombre(self):
        nombre_anterior = self.comite.nombre
        self.comite.nombre = 'comite-test-nombre-cambiado'
        self.comite.save()
        try:
            self.assertNotEqual(self.comite.nombre, nombre_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        


    def test_editar_descripcion(self):
        descripcion_anterior = self.comite.descripcion
        self.comite.descripcion = 'descripcion-cambiada-test'
        self.comite.save()
        try:
            self.assertNotEqual(self.comite.descripcion, descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))        



class ComiteTestEliminar(TestComiteSetUp):
    def setUp(self):
        super(ComiteTestEliminar, self).setUp()
        self.id_comite = self.comite.id

    def __del__(self):
        pass        

    def test_eliminar_comite(self):
        self.comite.delete()
        
# **Volver atras** : [[models.py]]

# **Ir a la documentación de URLS del modulo comité** : [[urls.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)

