from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Espaco

Usuario = get_user_model()


class CadastroEspacoTests(TestCase):

    def setUp(self):
        self.admin = Usuario.objects.create_user(
            'admin_teste', password='senha_teste_123',
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        self.aluno = Usuario.objects.create_user(
            'aluno_teste', password='senha_teste_123',
        )
        self.dados = {
            'nome': 'Laboratório 1',
            'tipo': 'Laboratório',
            'capacidade': 30,
            'recursos': 'Computadores',
            'localizacao': 'Bloco A',
        }

    def test_administrador_cadastra_espaco(self):
        self.client.force_login(self.admin)
        resposta = self.client.post('/espacos/cadastrar/', self.dados)

        self.assertRedirects(resposta, '/espacos/')
        self.assertTrue(Espaco.objects.filter(nome='Laboratório 1').exists())

    def test_capacidade_zero_invalida(self):
        self.client.force_login(self.admin)
        resposta = self.client.post(
            '/espacos/cadastrar/', {**self.dados, 'capacidade': 0}
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Espaco.objects.exists())

    def test_aluno_nao_cadastra_espaco(self):
        self.client.force_login(self.aluno)
        resposta = self.client.post('/espacos/cadastrar/', self.dados)

        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(Espaco.objects.exists())

    def test_superusuario_entra_como_administrador(self):
        su = Usuario.objects.create_superuser('root', 'root@exemplo.com', 'senha_teste_123')
        self.assertTrue(su.is_administrador())
