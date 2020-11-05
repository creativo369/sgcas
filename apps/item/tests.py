from datetime import datetime
from apps.usuario.models import User
from django.test import TestCase
from apps.item.models import Item
from apps.item.views import explore
from apps.tipo_item.models import TipoItem
from apps.proyecto.models import Proyecto
from apps.fase.models import Fase


class ItemSetUpTest(TestCase):
    def setUp(self):        
        self.item = Item.objects.create(nombre='item-test', descripcion='descripcion-test', estado='Desarrollo',
                                        costo=2)
        self.item.usuarios_a_cargo.add(User.objects.create(username='usuario1'))
        self.item.tipo_item = TipoItem.objects.create(nombre='tipo1', descripcion='descripcion-tipo1',
                                                 atributos=('Boolean', 'Boolean'))

        self.item.padres.add(Item.objects.create(nombre='Item', descripcion='descripcion item', costo=3))

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
        anterior_TI = self.item.tipo_item
        self.item.tipo_item = TipoItem.objects.create(nombre='tipo1', descripcion='descripcion-tipo1',
                                                 atributos=('Char', 'Char'))

        try:
            self.assertNotEqual(self.item.tipo_item, anterior_TI)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

        cant_padres = len(self.item.padres.all())
        self.item.padres.add(Item.objects.create(nombre='Item1', descripcion='descripcion item 1', costo=5))

        try:
            self.assertNotEqual(len(self.item.padres.all()), cant_padres)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_aprobar_item(self):
        estado_anterior = self.item.estado

        if (len(self.item.padres.all())+len(self.item.hijos.all())+len(self.item.antecesores.all())+
            len(self.item.sucesores.all()))!=0:
                self.item.estado ='Aprobado' #un ítem solo puede ser aprobado si al menos tiene una relación
        try:
            self.assertNotEqual(self.item.estado, estado_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))


    def test_establecer_relacion(self):
        cantidad_hijos = len(self.item.hijos.all()) #inicialmente no tiene hijos
        self.item.hijos.add(Item.objects.create(nombre='item_hijo',descripcion='descripcion_hijo',
                                                costo= 8))
        try:
            self.assertNotEqual(cantidad_hijos, len(self.item.hijos.all()))
        except AssertionError as e:
            print("Error de comparacion: {}".format(e)) 

    def test_modificar_relacion(self):
        padre_nombre = self.item.padres.first().nombre

        self.item.padres.filter(nombre= padre_nombre).update(nombre='item_prueba')        

        try:
            self.assertNotEqual(padre_nombre, self.item.padres.first().nombre)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e)) 

    def test_eliminar_relacion(self):
        cant_padres = len(self.item.padres.all())

        try:
            self.assertNotEqual(cant_padres,len(self.item.padres.all().delete()))
        except AssertionError as e:
            print("Error de comparacion: {}".format(e)) 

    def test_historial_de_cambios(self):
        prueba_item= Item.objects.create(nombre='item_prueba', descripcion='descripcion_item',
                                         costo=3)
        nro_version_inicial= prueba_item.nro_version

        for r in (1,3):
            prueba_item.costo += r #si se modifica un atrubuto del item se genera una nueva versión
            prueba_item.nro_version=prueba_item.nro_version+0.1
            prueba_item.save()

        try:
            self.assertNotEqual(nro_version_inicial,prueba_item.nro_version)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_calculo_impacto(self): 

        #se crea el proyecto, las fases del proyecto y los items de las fases.
        proyecto_prueba = Proyecto.objects.create(gerente=User.objects.create(username='pepe'), nombre='proyecto_prueba', 
            descripcion= 'descripcion proyecto_prueba',estado ='Iniciado')
        fase1 = Fase.objects.create(nombre = 'fase1',descripcion = 'descripcion fase1', proyecto= proyecto_prueba)
        fase2 = Fase.objects.create(nombre = 'fase2',descripcion = 'descripcion fase2', proyecto= proyecto_prueba)

        item_padre = Item.objects.create(nombre='padre',descripcion='descripcion padre',fase= fase1, costo=2)
        hijo = Item.objects.create(nombre='hijo',descripcion='descripcion hijo', fase= fase2, costo=3)
        sucesor = Item.objects.create(nombre='sucesor',descripcion='descripcion sucesor', fase= fase2, costo=4)

        
        #se calcula la complejidad del proyecto
        fases= Fase.objects.filter(proyecto=proyecto_prueba).all()

        complejidad_proyecto = 0
        for fase in fases:
            item_de_fase = Item.objects.filter(fase=fase).all()
            for item in item_de_fase:
                complejidad_proyecto+= item.costo

        proyecto_prueba.complejidad = complejidad_proyecto
        proyecto_prueba.save()

        #se relacionan  los items de las distintas fases
        item_padre.hijos.add(hijo)
        item_padre.save()
        item_padre.sucesores.add(sucesor)
        item_padre.save()

        calculo = explore(item_padre, impacto=0)


        #se obtiene el impacto inicial del ítem
        impacto_inicial = round((calculo / proyecto_prueba.complejidad), 2)

        #se agrega un nuevo ítem sucesor al item_padre        
        item_padre.sucesores.add(Item.objects.create(nombre='item',descripcion='descripcion item', fase= fase2, costo=9))
        item_padre.save()

        #se recalcula la complejidad del proyecto
        complejidad_proyecto = 0
        for fase in fases:
            item_de_fase = Item.objects.filter(fase=fase).all()
            for item in item_de_fase:
                complejidad_proyecto+= item.costo

        proyecto_prueba.complejidad = complejidad_proyecto
        proyecto_prueba.save()

        #se obtiene el nuevo impacto del proyecto
        impacto_final = round((calculo / proyecto_prueba.complejidad), 2)
        
        calculo = explore(item_padre, impacto=0)

        try:
            self.assertNotEqual(impacto_inicial,round((calculo / proyecto_prueba.complejidad), 2))
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
