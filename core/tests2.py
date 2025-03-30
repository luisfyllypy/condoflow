""" from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from jsonschema import ValidationError
from core.models import Aviso, Reserva, Profile
from django.contrib.messages import get_messages
import json

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
 """