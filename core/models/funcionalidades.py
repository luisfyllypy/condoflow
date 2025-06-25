from django.db import models

class Reserva(models.Model):
    """
    Representa a reserva de uma Área Comum por um Morador.
    """
    class SituacaoReserva(models.TextChoices):
        AGUARDANDO = 'AGUARDANDO', 'Aguardando Confirmação'
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        EFETIVADO = 'EFETIVADO', 'Efetivado (Utilizado)'

    morador_solicitante = models.ForeignKey(
        'core.RegistroMorador',
        on_delete=models.CASCADE,
        related_name="reservas_feitas",
        verbose_name="Morador Solicitante"
    )
    area_comum = models.ForeignKey(
        'core.AreaComum',
        on_delete=models.PROTECT,
        limit_choices_to={'reservavel': True},
        related_name="reservas",
        verbose_name="Área Comum"
    )
    funcionario_aprovador = models.ForeignKey(
        'core.RegistroFuncionario',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="reservas_aprovadas",
        verbose_name="Funcionário Aprovador"
    )
    data_reserva = models.DateTimeField(verbose_name="Data e Hora da Reserva")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    situacao = models.CharField(
        max_length=15,
        choices=SituacaoReserva.choices,
        default=SituacaoReserva.AGUARDANDO,
        verbose_name="Situação"
    )

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-data_reserva']

    def __str__(self):
        return f"Reserva de {self.area_comum.nome} por {self.morador_solicitante.pessoa.nome_completo}"


class Ocorrencia(models.Model):
    """
    Registra uma ocorrência aberta por um morador.
    """
    class SituacaoOcorrencia(models.TextChoices):
        AGUARDANDO = 'AGUARDANDO', 'Aguardando'
        CIENTE = 'CIENTE', 'Ciente'
        RESOLVIDO = 'RESOLVIDO', 'Resolvido'

    morador_relator = models.ForeignKey(
        'core.RegistroMorador',
        on_delete=models.CASCADE,
        related_name="ocorrencias_abertas",
        verbose_name="Morador Relator"
    )
    funcionario_responsavel = models.ForeignKey(
        'core.RegistroFuncionario',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="ocorrencias_atendidas",
        verbose_name="Funcionário Responsável"
    )
    titulo = models.CharField(max_length=50, verbose_name="Título")
    descricao = models.TextField(max_length=1000, verbose_name="Descrição")
    situacao = models.CharField(
        max_length=10,
        choices=SituacaoOcorrencia.choices,
        default=SituacaoOcorrencia.AGUARDANDO,
        verbose_name="Situação"
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo


class RegistroPonto(models.Model):
    """
    Registra a marcação de ponto de um funcionário em um local específico.
    """
    funcionario = models.ForeignKey(
        'core.RegistroFuncionario',
        on_delete=models.CASCADE,
        related_name="registros_ponto",
        verbose_name="Funcionário"
    )
    # Local onde o ponto foi batido (ex: portaria, administração).
    local = models.ForeignKey(
        'core.Endereco',
        on_delete=models.PROTECT,
        related_name="registros_ponto_local",
        verbose_name="Local do Ponto"
    )
    inicio = models.DateTimeField(verbose_name="Início do Turno")
    fim = models.DateTimeField(null=True, blank=True, verbose_name="Fim do Turno")

    class Meta:
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Ponto"
        ordering = ['-inicio']

    def __str__(self):
        return f"Ponto de {self.funcionario.pessoa.nome_completo} em {self.inicio.strftime('%d/%m/%Y %H:%M')}"
