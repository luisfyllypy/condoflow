from django.contrib import admin
from ..models import RegistroMorador, RegistroProprietario, RegistroFuncionario, RegistroVisitante

@admin.register(RegistroMorador)
class RegistroMoradorAdmin(admin.ModelAdmin):
    """ Admin para o modelo RegistroMorador. """
    list_display = ('pessoa', 'endereco', 'inicio', 'fim')
    list_filter = ('endereco', 'inicio')
    search_fields = ('pessoa__nome_completo', 'endereco__numero', 'endereco__casa__rua',
                     'endereco__apartamento__predio')

    # Adiciona uma navegação por datas no topo da lista.
    date_hierarchy = 'inicio'

    # Essencial para selecionar Pessoa e Endereço de forma inteligente.
    autocomplete_fields = ('pessoa', 'endereco')


@admin.register(RegistroProprietario)
class RegistroProprietarioAdmin(admin.ModelAdmin):
    """ Admin para o modelo RegistroProprietario. """
    list_display = ('pessoa', 'endereco', 'data_compra', 'data_venda')
    list_filter = ('endereco',)
    search_fields = ('pessoa__nome_completo', 'endereco__numero')
    date_hierarchy = 'data_compra'
    autocomplete_fields = ('pessoa', 'endereco')


@admin.register(RegistroFuncionario)
class RegistroFuncionarioAdmin(admin.ModelAdmin):
    """ Admin para o modelo RegistroFuncionario. """
    list_display = ('pessoa', 'cargo', 'data_admissao', 'data_demissao')

    # O filtro por 'cargo' é muito útil aqui.
    list_filter = ('cargo',)
    search_fields = ('pessoa__nome_completo',)
    date_hierarchy = 'data_admissao'
    autocomplete_fields = ('pessoa',)


@admin.register(RegistroVisitante)
class RegistroVisitanteAdmin(admin.ModelAdmin):
    """ Admin para o modelo RegistroVisitante. """
    list_display = ('pessoa_visitante', 'morador_responsavel', 'endereco_destino', 'data_chegada')
    list_filter = ('endereco_destino', 'data_chegada')

    # Busca poderosa que permite encontrar pelo nome do visitante, do morador ou pelo endereço.
    search_fields = (
        'pessoa_visitante__nome_completo',
        'morador_responsavel__pessoa__nome_completo',
        'endereco_destino__numero',
    )
    date_hierarchy = 'data_chegada'

    # Autocomplete para todos os campos de relacionamento.
    autocomplete_fields = ('pessoa_visitante', 'morador_responsavel', 'endereco_destino')