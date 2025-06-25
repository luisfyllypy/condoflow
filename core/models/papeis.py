from django.db import models

class RegistroMorador(models.Model):
    """
    Registra o período em que uma Pessoa foi moradora de um determinado Endereço.
    """
    pessoa = models.ForeignKey(
        'core.Pessoa',
        on_delete=models.CASCADE,
        related_name="registros_morador",
        verbose_name="Pessoa"
    )
    endereco = models.ForeignKey(
        'core.Endereco',
        on_delete=models.PROTECT,  # Proteger para não apagar um endereço com histórico de moradores.
        related_name="registros_morador",
        verbose_name="Endereço"
    )
    inicio = models.DateField(verbose_name="Início da Residência")
    fim = models.DateField(
        null=True, blank=True,  # Permitir nulo para moradores atuais, sem data de saída.
        verbose_name="Fim da Residência"
    )

    class Meta:
        verbose_name = "Registro de Morador"
        verbose_name_plural = "Registros de Moradores"
        ordering = ['-inicio']

    def __str__(self):
        return f"{self.pessoa.nome_completo} em {self.endereco}"


class RegistroProprietario(models.Model):
    """
    Registra o período em que uma Pessoa foi proprietária de um Endereço.
    """
    pessoa = models.ForeignKey(
        'core.Pessoa',
        on_delete=models.CASCADE,
        related_name="registros_proprietario",
        verbose_name="Pessoa"
    )
    endereco = models.ForeignKey(
        'core.Endereco',
        on_delete=models.PROTECT,  # Proteger para não apagar um endereço com histórico.
        related_name="registros_proprietario",
        verbose_name="Endereço"
    )
    data_compra = models.DateField(verbose_name="Data da Compra")
    data_venda = models.DateField(null=True, blank=True, verbose_name="Data da Venda")

    class Meta:
        verbose_name = "Registro de Proprietário"
        verbose_name_plural = "Registros de Proprietários"
        ordering = ['-data_compra']

    def __str__(self):
        return f"Proprietário {self.pessoa.nome_completo} de {self.endereco}"


class RegistroFuncionario(models.Model):
    """
    Registra o período de trabalho de uma Pessoa como funcionário do condomínio.
    """
    class Cargos(models.TextChoices):
        SINDICO = 'SINDICO', 'Síndico'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        PORTEIRO = 'PORTEIRO', 'Porteiro'
        SERVICOS_GERAIS = 'SERVICOS_GERAIS', 'Serviços Gerais'

    pessoa = models.ForeignKey(
        'core.Pessoa',
        on_delete=models.CASCADE,
        related_name="registros_funcionario",
        verbose_name="Pessoa"
    )
    cargo = models.CharField(max_length=20, choices=Cargos.choices, verbose_name="Cargo")
    data_admissao = models.DateField(verbose_name="Data de Admissão")
    data_demissao = models.DateField(null=True, blank=True, verbose_name="Data de Demissão")

    class Meta:
        verbose_name = "Registro de Funcionário"
        verbose_name_plural = "Registros de Funcionários"
        ordering = ['-data_admissao']

    def __str__(self):
        return f"Funcionário {self.pessoa.nome_completo} - {self.get_cargo_display()}"


class RegistroVisitante(models.Model):
    """
    Registra uma visita pontual de uma Pessoa a um Endereço,
    autorizada por uma Pessoa responsável (morador).
    """
    pessoa_visitante = models.ForeignKey(
        'core.Pessoa',
        on_delete=models.CASCADE,
        related_name="visitas_feitas",
        verbose_name="Visitante"
    )
    # A pessoa do condomínio morador que autorizou a entrada.
    morador_responsavel = models.ForeignKey(
        RegistroMorador,
        on_delete=models.PROTECT,  # Não apagar um registro de morador se ele autorizou visitas.
        related_name="visitas_autorizadas",
        verbose_name="Morador Responsável"
    )
    # O local exato da visita (pode ser uma casa, apto, ou uma área comum).
    endereco_destino = models.ForeignKey(
        'core.Endereco',
        on_delete=models.PROTECT,
        related_name="visitas_recebidas",
        verbose_name="Endereço de Destino"
    )
    data_chegada = models.DateTimeField(verbose_name="Data e Hora da Chegada")

    class Meta:
        verbose_name = "Registro de Visitante"
        verbose_name_plural = "Registros de Visitantes"
        ordering = ['-data_chegada']

    def __str__(self):
        return f"Visita de {self.pessoa_visitante.nome_completo} a {self.endereco_destino}"