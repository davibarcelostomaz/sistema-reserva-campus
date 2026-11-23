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


class AnaliseECancelamentoTests(TestCase):

    def setUp(self):
        Usuario = get_user_model()
        self.admin = Usuario.objects.create_user(
            'admin_teste', password='senha_teste_123',
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        self.aluno = Usuario.objects.create_user(
            'aluno_teste', password='senha_teste_123',
        )
        self.professor = Usuario.objects.create_user(
            'prof_teste', password='senha_teste_123',
            perfil=Usuario.Perfil.PROFESSOR,
        )
        self.espaco = Espaco.objects.create(
            nome='Sala 101', tipo='Sala', capacidade=40, localizacao='Bloco B'
        )
        self.data = date.today() + timedelta(days=3)

    def criar_reserva(self, usuario, inicio, fim, status=Reserva.Status.PENDENTE):
        return Reserva.objects.create(
            usuario=usuario, espaco=self.espaco, data=self.data,
            hora_inicio=inicio, hora_fim=fim, status=status,
        )

    def test_reserva_de_professor_entra_aprovada(self):
        reserva = self.criar_reserva(self.professor, time(8, 0), time(9, 0))
        self.assertEqual(reserva.status, Reserva.Status.APROVADA)

    def test_administrador_aprova_reserva(self):
        reserva = self.criar_reserva(self.aluno, time(10, 0), time(11, 0))
        self.client.force_login(self.admin)
        self.client.post(f'/reservas/{reserva.id}/aprovar/')
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.Status.APROVADA)

    def test_administrador_recusa_reserva(self):
        reserva = self.criar_reserva(self.aluno, time(10, 0), time(11, 0))
        self.client.force_login(self.admin)
        self.client.post(f'/reservas/{reserva.id}/recusar/')
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.Status.RECUSADA)

    def test_aluno_nao_analisa_reservas(self):
        reserva = self.criar_reserva(self.aluno, time(10, 0), time(11, 0))
        self.client.force_login(self.aluno)
        self.assertEqual(self.client.get('/reservas/pendentes/').status_code, 403)
        self.assertEqual(
            self.client.post(f'/reservas/{reserva.id}/aprovar/').status_code, 403
        )

    def test_usuario_cancela_propria_reserva(self):
        reserva = self.criar_reserva(self.aluno, time(10, 0), time(11, 0))
        self.client.force_login(self.aluno)
        self.client.post(f'/reservas/{reserva.id}/cancelar/')
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.Status.CANCELADA)

    def test_nao_cancela_reserva_recusada(self):
        reserva = self.criar_reserva(
            self.aluno, time(10, 0), time(11, 0), Reserva.Status.RECUSADA
        )
        self.client.force_login(self.aluno)
        self.client.post(f'/reservas/{reserva.id}/cancelar/')
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.Status.RECUSADA)

    def test_nao_cancela_reserva_de_outro_usuario(self):
        reserva = self.criar_reserva(self.professor, time(10, 0), time(11, 0))
        self.client.force_login(self.aluno)
        resposta = self.client.post(f'/reservas/{reserva.id}/cancelar/')
        self.assertEqual(resposta.status_code, 404)
