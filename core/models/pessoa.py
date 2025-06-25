from django.db import models
from django.conf import settings

class Pessoa(models.Model):
    """
    Representa uma pessoa física no sistema, com seus dados pessoais básicos.
    Esta tabela é a "mãe" de todos os papéis que uma pessoa pode exercer
    no condomínio.
    """

    # O CPF será a chave primária, garantindo que cada pessoa seja única.
    # Usamos CharField para manter zeros à esquerda, se houver.
    cpf = models.CharField(max_length=11, primary_key=True, verbose_name="CPF")
    nome_completo = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")

    # E-mail da pessoa. É único para evitar duplicidade, mas pode ser nulo
    # pois nem toda pessoa cadastrada (ex: um visitante rápido) terá um e-mail.
    email = models.EmailField(
        max_length=50,
        unique=True,
        null=True,        # Permite que o valor seja NULL no banco de dados.
        blank=True,       # Permite que o campo seja em branco nos formulários.
        verbose_name="E-mail"
    )

    # --- A LIGAÇÃO CRUCIAL ---
    # Este é o relacionamento um-para-um com o modelo de Usuário.
    # Uma Pessoa PODE ou NÃO TER um Usuário para login.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,    # Forma correta de referenciar o seu modelo 'Usuario'.
        on_delete=models.SET_NULL,   # Se o usuário for deletado, não apague a Pessoa. Apenas anule a ligação.
        null=True,                   # Permite que a coluna no banco seja nula.
        blank=True,                  # Permite que o campo seja opcional em formulários.
        related_name='pessoa',       # ESSENCIAL: Permite o acesso reverso: usuario.pessoa
        verbose_name="Usuário do Sistema"
    )

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo