from django.test import TestCase
from django.contrib.auth.models import User


class UsuarioTestCrear(TestCase):
    def setUp(self):
        self.username_modificado = 'username-modificado'
        self.usuario = User.objects.create(username='user-test')
        print('Usuario creado OK')

    def test_usuario_crear(self):
        self.assertEqual(self.usuario.username, 'user-test')
        print('Usuario-test_usuario_crear OK')

    def test_usuario_modificar(self):
        username_anterior = self.usuario.username
        self.usuario.username = 'username_modificado'
        self.usuario.save()
        self.assertNotEqual(self.usuario.username, username_anterior)
        print('Usuario-test_usuario_modificar OK')

    def test_eliminar_usuario(self):
        self.usuario.delete()

    def __del__(self):
        print('Usuario borrado OK')

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>
