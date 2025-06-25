from django.db import models
from django.db.models import Q

class Telefone(models.Model):
    """
    Representa um número de telefone.
    Um telefone deve pertencer OU a uma Pessoa OU a um Endereço, mas não a ambos.
    """
    class TipoTelefone(models.TextChoices):
        FIXO = 'FIXO', 'Fixo'
        CELULAR = 'CELULAR', 'Celular'

    numero = models.CharField(max_length=15, verbose_name="Número")
    tipo = models.CharField(max_length=7, choices=TipoTelefone.choices, default=TipoTelefone.CELULAR, verbose_name="Tipo")
    pessoa = models.ForeignKey(
        'core.Pessoa',
        on_delete=models.CASCADE,
        related_name='telefones',
        null=True,
        blank=True,
        verbose_name="Pessoa"
    )
    endereco = models.ForeignKey(
        'core.Endereco',
        on_delete=models.CASCADE,
        related_name='telefones',
        null=True,
        blank=True,
        verbose_name="Endereço"
    )

    class Meta:
        verbose_name = "Telefone"
        verbose_name_plural = "Telefones"
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(pessoa__isnull=False) & Q(endereco__isnull=True) |
                    Q(pessoa__isnull=True) & Q(endereco__isnull=False)
                ),
                name='telefone_pertence_a_pessoa_ou_endereco'
            )
        ]

    def __str__(self):
        return f"{self.numero} ({self.get_tipo_display()})"