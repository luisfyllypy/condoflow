import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    """
    Manager para o nosso modelo de usuário personalizado.
    Inclui uma função para limpar o CPF, garantindo que apenas dígitos sejam salvos.
    """

    def _limpar_cpf(self, cpf):
        """ Remove a pontuação de uma string de CPF. """
        return ''.join(re.findall(r'\d', str(cpf)))

    def create_user(self, cpf, password=None, **extra_fields):
        """ Cria e salva um usuário comum com o CPF e senha fornecidos. """
        if not cpf:
            raise ValueError('O CPF é obrigatório.')

        cpf_limpo = self._limpar_cpf(cpf)
        if len(cpf_limpo) != 11:
            raise ValidationError("CPF deve conter 11 dígitos.")

        user = self.model(cpf=cpf_limpo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        """ Cria e salva um superusuário. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True.')

        return self.create_user(cpf, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário principal do sistema.
    Usa CPF como login e não possui campo de email.
    """
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")

    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Acesso de Equipe")
    # is_superuser, groups e user_permissions já são fornecidos pelo PermissionsMixin

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    objects = UsuarioManager()

    USERNAME_FIELD = 'cpf'

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.cpf}"

    @property
    def cpf_formatado(self):
        """ Retorna o CPF formatado para exibição. """
        if self.cpf:
            return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"
        return ""