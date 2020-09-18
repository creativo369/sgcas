from django.test import TestCase
from apps.usuario.models import User



class UsuarioTestCrear(TestCase):
    def setUp(self):
        self.username_modificado = 'username-modificado'
        self.usuario = User.objects.create(username='user-test')
        

    def test_usuario_crear(self):        
        self.assertEqual(self.usuario.username, 'user-test')
      

    def test_usuario_modificar(self):
        username_anterior = self.usuario.username
        self.usuario.username = 'username_modificado'
        self.usuario.save()
        self.assertNotEqual(self.usuario.username, username_anterior)

       
    def test_eliminar_usuario(self):
        self.usuario.delete()

    def __del__(self):
        pass
        

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)