from datetime import date, timedelta, time

from django.contrib.auth import get_user_model
from django.test import TestCase

from espacos.models import Espaco
from .forms import SolicitacaoReservaForm
from .models import Reserva


class SolicitacaoReservaFormTests(TestCase):

    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username='aluno_teste',
            password='senha_teste_123'
        )

        self.espaco = Espaco.objects.create(
            nome='Laboratório de Teste',
            tipo='Laboratório',
            capacidade=30,
            recursos='Computadores',
            localizacao='Bloco A'
        )

        self.data_reserva = date.today() + timedelta(days=7)

        Reserva.objects.create(
            usuario=self.usuario,
            espaco=self.espaco,
            data=self.data_reserva,
            hora_inicio=time(14, 0),
            hora_fim=time(16, 0),
            status=Reserva.Status.PENDENTE
        )

    def criar_formulario(self, inicio, fim):
        return SolicitacaoReservaForm(data={
            'espaco': self.espaco.id,
            'data': self.data_reserva.isoformat(),
            'hora_inicio': inicio,
            'hora_fim': fim,
        })

    def test_impede_reserva_sobreposta(self):
        formulario = self.criar_formulario('15:00', '17:00')

        self.assertFalse(formulario.is_valid())
        self.assertIn(
            'Este espaço já possui uma reserva',
            str(formulario.errors)
        )

    def test_permite_horarios_consecutivos(self):
        formulario = self.criar_formulario('16:00', '18:00')

        self.assertTrue(formulario.is_valid())

    def test_permite_horario_de_reserva_cancelada(self):
        Reserva.objects.filter(
            espaco=self.espaco
        ).update(status=Reserva.Status.CANCELADA)

        formulario = self.criar_formulario('14:00', '16:00')

        self.assertTrue(formulario.is_valid())

    def test_impede_data_passada(self):
        formulario = SolicitacaoReservaForm(data={
            'espaco': self.espaco.id,
            'data': (date.today() - timedelta(days=1)).isoformat(),
            'hora_inicio': '10:00',
            'hora_fim': '12:00',
        })

        self.assertFalse(formulario.is_valid())
        self.assertIn(
            'Não é possível reservar uma data passada.',
            str(formulario.errors)
        )

    def test_impede_horario_final_anterior(self):
        formulario = self.criar_formulario('16:00', '14:00')

        self.assertFalse(formulario.is_valid())
        self.assertIn(
            'O horário de término deve ser posterior ao início.',
            str(formulario.errors)
        )

    def test_impede_horarios_iguais(self):
        formulario = self.criar_formulario('14:00', '14:00')

        self.assertFalse(formulario.is_valid())
        self.assertIn(
            'O horário de término deve ser posterior ao início.',
            str(formulario.errors)
        )

    def test_usuario_autenticado_consegue_solicitar_reserva(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(
            '/reservas/solicitar/',
            data={
                'espaco': self.espaco.id,
                'data': self.data_reserva.isoformat(),
                'hora_inicio': '10:00',
                'hora_fim': '12:00',
            }
        )

        self.assertEqual(resposta.status_code, 302)

        reserva = Reserva.objects.get(
            espaco=self.espaco,
            data=self.data_reserva,
            hora_inicio=time(10, 0),
        )

        self.assertEqual(reserva.usuario, self.usuario)
        self.assertEqual(reserva.status, Reserva.Status.PENDENTE)

    def test_usuario_nao_autenticado_nao_pode_solicitar_reserva(self):
        resposta = self.client.get('/reservas/solicitar/')

        self.assertEqual(resposta.status_code, 302)
        self.assertIn('/login/', resposta.url)
