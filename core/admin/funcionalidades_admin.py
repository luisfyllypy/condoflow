from django.contrib import admin
from ..models import Reserva, Ocorrencia, RegistroPonto

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """ Admin para o modelo Reserva. """
    list_display = ('area_comum', 'morador_solicitante', 'data_reserva', 'situacao')
    list_filter = ('situacao', 'area_comum', 'data_reserva')
    search_fields = (
        'morador_solicitante__pessoa__nome_completo',
        'area_comum__nome',
        'funcionario_aprovador__pessoa__nome_completo'
    )
    date_hierarchy = 'data_reserva'
    autocomplete_fields = ('morador_solicitante', 'area_comum', 'funcionario_aprovador')

    # Organiza o formulário de edição em seções lógicas.
    fieldsets = (
        ('Detalhes da Reserva', {
            'fields': ('morador_solicitante', 'area_comum', 'data_reserva')
        }),
        ('Status e Aprovação', {
            'fields': ('situacao', 'funcionario_aprovador')
        }),
        ('Datas de Controle (Automático)', {
            # Deixa as datas de controle visíveis, mas não editáveis.
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)  # Oculta a seção por padrão para um form mais limpo.
        }),
    )

    # Torna os campos de data automática apenas de leitura.
    readonly_fields = ('data_criacao', 'data_atualizacao')


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    """ Admin para o modelo Ocorrencia. """
    list_display = ('titulo', 'morador_relator', 'situacao', 'funcionario_responsavel', 'data_criacao')
    list_filter = ('situacao', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'morador_relator__pessoa__nome_completo')
    date_hierarchy = 'data_criacao'
    autocomplete_fields = ('morador_relator', 'funcionario_responsavel')
    readonly_fields = ('data_criacao', 'data_atualizacao')

    fieldsets = (
        ('Detalhes da Ocorrência', {
            'fields': ('titulo', 'descricao', 'morador_relator')
        }),
        ('Atendimento e Status', {
            'fields': ('situacao', 'funcionario_responsavel')
        }),
        ('Datas de Controle (Automático)', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RegistroPonto)
class RegistroPontoAdmin(admin.ModelAdmin):
    """ Admin para o modelo RegistroPonto. """
    list_display = ('funcionario', 'local', 'inicio', 'fim')
    list_filter = ('local', 'inicio')
    search_fields = ('funcionario__pessoa__nome_completo', 'local__numero')
    date_hierarchy = 'inicio'
    autocomplete_fields = ('funcionario', 'local')