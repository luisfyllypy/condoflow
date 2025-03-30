from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

class Reserva(models.Model):
    AREAS_CHOICES = [
        ('churrasqueira', 'Churrasqueira'),
        ('piscina', 'Piscina'),
        ('quadra', 'Quadra de Esporte'),
        ('sala-de-jogos', 'Sala de Jogos'),
        ('salao-de-festa', 'Salão de Festas'),
    ]
    
    BLOCO_CHOICES = [
        ('A', 'Bloco A'),
        ('B', 'Bloco B'),
        ('C', 'Bloco C'),
        ('D', 'Bloco D'),
        ('E', 'Bloco E'),
    ]

    area = models.CharField(max_length=20, choices=AREAS_CHOICES)
    data = models.DateField()
    hora = models.TimeField(blank=True, null=True)  # Apenas para áreas que exigem horário
    bloco = models.CharField(max_length=1, choices=BLOCO_CHOICES, blank=True, null=True)  # Apenas para salão de festas
    usuario_nome = models.CharField(max_length=100, default="Usuário Desconhecido")

    def save(self, *args, **kwargs):
        if self.area in ['churrasqueira', 'piscina']:
            reservas_no_dia = Reserva.objects.filter(area=self.area, data=self.data).count()
            if reservas_no_dia >= 10:
                raise ValidationError("Limite diário de reservas para esta área atingido.")
        elif self.area in ['quadra', 'sala-de-jogos']:
            reservas_no_horario = Reserva.objects.filter(area=self.area, data=self.data, hora=self.hora).count()
            if reservas_no_horario >= 2:
                raise ValidationError("Limite de 2 reservas por horário para esta área atingido.")
        elif self.area == 'salao-de-festa':
            if not self.bloco:
                raise ValidationError("Selecione o bloco para o salão de festas.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.area} - {self.data} ({self.hora} - {self.usuario_nome})"


class Aviso(models.Model):
    titulo = models.CharField(max_length=100)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('F', 'Funcionário'),
        ('M', 'Morador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username
