from django.db import models

# Modelos de Endereço (Herança Multi-tabela)
class Endereco(models.Model):
    """
    MODELO PAI - Representa um endereço genérico no condomínio.
    Não se cria um 'Endereco' diretamente, mas sim um de seus filhos
    (Casa, Apartamento ou AreaComum).
    """

    class TipoEndereco(models.TextChoices):
        CASA = 'CASA', 'Casa'
        APARTAMENTO = 'APARTAMENTO', 'Apartamento'
        AREA_COMUM = 'AREA_COMUM', 'Área Comum'

    numero = models.IntegerField(verbose_name="Número")
    tipo = models.CharField(max_length=12, choices=TipoEndereco.choices, verbose_name="Tipo")

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        # Tenta obter uma representação mais específica do modelo filho.
        if hasattr(self, 'casa'):
            return str(self.casa)
        if hasattr(self, 'apartamento'):
            return str(self.apartamento)
        if hasattr(self, 'areacomum'):
            return str(self.areacomum)
        return f"Endereço genérico nº {self.numero}"


class Casa(Endereco):
    """ MODELO FILHO - Especialização de Endereço para uma casa. """
    rua = models.CharField(max_length=50, verbose_name="Rua")
    conjunto = models.CharField(max_length=50, blank=True, null=True, verbose_name="Conjunto")

    class Meta:
        verbose_name = "Casa"
        verbose_name_plural = "Casas"

    def __str__(self):
        return f"Casa nº {self.numero}, Rua {self.rua}"


class Apartamento(Endereco):
    """ MODELO FILHO - Especialização de Endereço para um apartamento. """
    andar = models.CharField(max_length=50, verbose_name="Andar")
    predio = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prédio/Bloco")

    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"

    def __str__(self):
        return f"Apto nº {self.numero}, Andar {self.andar}"


class AreaComum(Endereco):
    """ MODELO FILHO - Especialização de Endereço para uma área comum. """
    nome = models.CharField(max_length=20, verbose_name="Nome da Área")
    reservavel = models.BooleanField(default=False, verbose_name="É Reservável?")
    descricao = models.TextField(max_length=1000, verbose_name="Descrição")
    local = models.CharField(max_length=100, blank=True, null=True, verbose_name="Localização")
    lotacao = models.IntegerField(blank=True, null=True, verbose_name="Lotação Máxima")

    class Meta:
        verbose_name = "Área Comum"
        verbose_name_plural = "Áreas Comuns"

    def __str__(self):
        return self.nome