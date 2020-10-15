from django.test import TestCase
from apps.usuario.models import User
from apps.proyecto.models import Proyecto
from apps.fase.models import Fase

class TestProyectoSetUp(TestCase):
    def setUp(self):
        self.proyecto= Proyecto.objects.create(gerente=User.objects.create(username='Pepe'), 
                                                nombre= 'proyecto-prueba', 
                                                descripcion= 'descripcion-proyecto-prueba' )
        self.proyecto.miembros.add(User.objects.create(username= 'Maria'))


class ProyectoTestCrear(TestProyectoSetUp):

    def setUp(self):
        super(ProyectoTestCrear, self).setUp()

    def test_nombre(self):
        try:
            self.assertEqual(self.proyecto.nombre, 'proyecto-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_descripcion(self):
        try:
            self.assertEqual(self.proyecto.descripcion, 'descripcion-proyecto-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))


class ProyectoTestEditar(TestProyectoSetUp):

    def setUp(self):
        super(ProyectoTestEditar, self).setUp()
        self.proyecto.gerente = User.objects.create(username='gerente2')

    def test_editar_nombre(self):
        nombre_anterior = self.proyecto.nombre
        self.proyecto.nombre = 'Proyecto-test-nombre-cambiado'
        try:
            self.assertNotEqual(self.proyecto.nombre, nombre_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_editar_descripcion(self):
        descripcion_anterior = self.proyecto.descripcion
        self.proyecto.descripcion = 'descripcion-cambiada-test'
        try:
            self.assertNotEqual(self.proyecto.descripcion, descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_agregar_y_eliminar_miembros(self):
        #Agregar miembros
        for r in 'abc':    
          self.proyecto.miembros.add(User.objects.create(username='Pepe'+r))

        try:
            self.assertEqual(len(self.proyecto.miembros.all()),4)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

        #Eliminar miembros    
        cantidad_miembros= len(self.proyecto.miembros.all())

        try:
            self.assertNotEqual(len(self.proyecto.miembros.first().delete()),cantidad_miembros)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_cerrar_proyecto(self):
        estado_anterior = self.proyecto.estado

        for r in 'abc':
            Fase.objects.create(nombre='fase'+r, descripcion='descripcion'+r, proyecto=self.proyecto,
                                estado='Cerrada')
        #se agregan las fases al proyecto

        fases_de_proyecto= Fase.objects.filter(proyecto=self.proyecto)

        no_cerrada = 0

        for fase in fases_de_proyecto:
            if not fase.estado=='Cerrada':
                no_cerrada +=1  #se verifica si todas la fases del proyecto estan 'Cerradas'

        if no_cerrada == 0:
            self.proyecto.estado = 'Finalizado'

        try:
            self.assertNotEqual(self.proyecto.estado,estado_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

class ProyectoTestEliminar(TestProyectoSetUp):
    def setUp(self):
        super(ProyectoTestEliminar, self).setUp()
        self.id_proyecto = self.proyecto.id

    def __del__(self):
        pass        

    def test_eliminar_proyecto(self):
        self.proyecto.delete()

# **Volver atras** : [[models.py]]

# **Ir a la documentación de la URL de la Aplicación** :[[urls.py]]

# === Indice de la documentación de la Aplicación Proyecto  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
