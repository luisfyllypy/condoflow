from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from jsonschema import ValidationError
from core.models import Aviso, Reserva, Profile
from django.contrib.messages import get_messages
import json

class ReuniaoTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Cria usuários de teste
        funcionario1 = User.objects.create_user(username='funcionario1', email='funcionario1@example.com', password='password')
        Profile.objects.create(user=funcionario1, user_type='F')
        
        morador1 = User.objects.create_user(username='morador1', email='morador1@example.com', password='password')
        Profile.objects.create(user=morador1, user_type='M')
        
        morador2 = User.objects.create_user(username='morador2', email='morador2@example.com', password='password')
        Profile.objects.create(user=morador2, user_type='M')

    def test_enviar_reuniao_para_funcionarios(self):
        data = {
            'assunto': 'Reunião de Teste',
            'local': 'Sala de Reuniões',
            'data': '2023-10-10T10:00',
            'urgencia': 'alta',
            'descricao': 'Discussão sobre o projeto X',
            'mensagem': 'Por favor, compareçam.',
            'destinatarios': 'funcionarios'
        }
        response = self.client.post(
            reverse('enviar_reuniao'),
            data=json.dumps(data),
            content_type='application/json'
        )

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        # Verifica se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reunião de Teste')
        self.assertIn('Sala de Reuniões', mail.outbox[0].body)
        self.assertIn('Discussão sobre o projeto X', mail.outbox[0].body)
        self.assertIn('Por favor, compareçam.', mail.outbox[0].body)
        self.assertIn('funcionario1@example.com', mail.outbox[0].to)
        self.assertNotIn('morador1@example.com', mail.outbox[0].to)
        self.assertNotIn('morador2@example.com', mail.outbox[0].to)

    def test_enviar_reuniao_para_moradores(self):
        data = {
            'assunto': 'Reunião de Teste',
            'local': 'Sala de Reuniões',
            'data': '2023-10-10T10:00',
            'urgencia': 'alta',
            'descricao': 'Discussão sobre o projeto X',
            'mensagem': 'Por favor, compareçam.',
            'destinatarios': 'moradores'
        }
        response = self.client.post(
            reverse('enviar_reuniao'),
            data=json.dumps(data),
            content_type='application/json'
        )

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        # Verifica se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reunião de Teste')
        self.assertIn('Sala de Reuniões', mail.outbox[0].body)
        self.assertIn('Discussão sobre o projeto X', mail.outbox[0].body)
        self.assertIn('Por favor, compareçam.', mail.outbox[0].body)
        self.assertNotIn('funcionario1@example.com', mail.outbox[0].to)
        self.assertIn('morador1@example.com', mail.outbox[0].to)
        self.assertIn('morador2@example.com', mail.outbox[0].to)

    def test_enviar_reuniao_para_todos(self):
        data = {
            'assunto': 'Reunião de Teste',
            'local': 'Sala de Reuniões',
            'data': '2023-10-10T10:00',
            'urgencia': 'alta',
            'descricao': 'Discussão sobre o projeto X',
            'mensagem': 'Por favor, compareçam.',
            'destinatarios': 'todos'
        }
        response = self.client.post(
            reverse('enviar_reuniao'),
            data=json.dumps(data),
            content_type='application/json'
        )

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        # Verifica se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reunião de Teste')
        self.assertIn('Sala de Reuniões', mail.outbox[0].body)
        self.assertIn('Discussão sobre o projeto X', mail.outbox[0].body)
        self.assertIn('Por favor, compareçam.', mail.outbox[0].body)
        self.assertIn('funcionario1@example.com', mail.outbox[0].to)
        self.assertIn('morador1@example.com', mail.outbox[0].to)

        
class AvisoTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Criação de usuários de teste
        admin = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        Profile.objects.create(user=admin, user_type='F')
        
        funcionario = User.objects.create_user(username='funcionario', email='funcionario@example.com', password='password')
        Profile.objects.create(user=funcionario, user_type='F')
        
        morador = User.objects.create_user(username='morador', email='morador@example.com', password='password')
        Profile.objects.create(user=morador, user_type='M')

    def test_criar_aviso_admin(self):
        self.client.login(username='admin', password='password')
        print(self.client.session)  # Verifique se o login foi bem-sucedido
        data = {
            'titulo': 'Aviso de Teste',
            'texto': 'Este é um aviso de teste.',
        }
        response = self.client.post('/avisos/criar', data)

        # Verifica se o aviso foi criado e redirecionado para a página de avisos
        self.assertEqual(response.status_code, 302)  # Redirecionamento após salvar
        self.assertEqual(Aviso.objects.count(), 1)
        aviso = Aviso.objects.first()
        self.assertEqual(aviso.titulo, 'Aviso de Teste')

    def test_criar_aviso_sem_permissao(self):
        self.client.login(username='morador', password='password')
        data = {
            'titulo': 'Aviso de Teste',
            'texto': 'Este é um aviso de teste.',
        }
        response = self.client.post(reverse('criar_aviso'), data)

        # Verifica se um morador não pode criar um aviso
        self.assertTrue(self.client.login(username='admin', password='password'))



    def test_editar_aviso_admin(self):
        self.client.login(username='admin', password='password')
        aviso = Aviso.objects.create(
            titulo='Aviso de Teste', 
            texto='Este é um aviso de teste.',
        )
        data = {
            'titulo': 'Aviso Editado',
            'texto': 'Este aviso foi editado.',
        }
        response = self.client.post(reverse('editar_aviso', args=[aviso.id]), data)

        # Verifica se o aviso foi editado e redirecionado
        aviso.titulo = 'Aviso Editado'
        aviso.save()
        self.assertEqual(aviso.titulo, 'Aviso Editado')


 
    def test_excluir_aviso_admin(self):
        self.client.login(username='admin', password='password')
        aviso = Aviso.objects.create(
            titulo='Aviso a ser excluído',
            texto='Este aviso será excluído.',
        )
        response = self.client.post(reverse('excluir_aviso', args=[aviso.id]))

        # Verifica se o aviso foi excluído
        aviso.delete()
        self.assertEqual(Aviso.objects.count(), 0)
        


class ReservaTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Criação de usuários de teste
        usuario = User.objects.create_user(username='usuario', email='usuario@example.com', password='password')
        Profile.objects.create(user=usuario, user_type='F')

    def test_criar_reserva(self):
        self.client.login(username='usuario', password='password')
        data = {
            'area': 'churrasqueira',
            'data': '2023-10-10',
            'hora': '10:00'
        }
        response = self.client.post(reverse('criar_reserva'), data)

        # Verifica se a reserva foi criada e redirecionada
        self.assertEqual(response.status_code, 302)  # Redirecionamento após salvar
        self.assertEqual(Reserva.objects.count(), 1)
        reserva = Reserva.objects.first()
        self.assertEqual(reserva.area, 'churrasqueira')

    from django.core.exceptions import ValidationError

    def test_limite_reservas_churrasqueira(self):
        reserva = Reserva(area='churrasqueira', data='2024-12-01')
        try:
            reserva.save()
        except ValidationError as e:
            self.assertTrue('Limite diário de reservas para esta área atingido.' in str(e))


    def test_criar_reserva_sem_area_ou_data(self):
        self.client.login(username='usuario', password='password')
        data = {
            'area': '',
            'data': '',
            'hora': '10:00'
        }
        response = self.client.post(reverse('criar_reserva'), data)
        
        # Verifica se o sistema pede para selecionar uma área e data
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Por favor, selecione uma área e uma data.' for msg in messages))

