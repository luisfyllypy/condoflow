# endereco_admin.py (Atualizado)

from django.contrib import admin
from ..models import Endereco, Casa, Apartamento, AreaComum


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Pai 'Endereco'.
    Serve como uma lista unificada de todos os tipos de endereço.
    A criação e edição direta por aqui são desabilitadas.
    """
    list_display = ('__str__', 'tipo', 'numero')
    list_filter = ('tipo',)
    search_fields = ('numero',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Casa)
class CasaAdmin(admin.ModelAdmin):
    """ Admin para o modelo Casa. """
    list_display = ('__str__', 'rua', 'conjunto')
    search_fields = ('numero', 'rua', 'conjunto')

    # NOVO: Torna o campo 'tipo' imutável nos formulários de adicionar e editar.
    readonly_fields = ('tipo',)

    fieldsets = (
        ('Dados Gerais (Endereço)', {
            # O campo 'tipo' continua aqui para ser exibido, mas agora como leitura.
            'fields': ('numero', 'tipo')
        }),
        ('Detalhes da Casa', {
            'fields': ('rua', 'conjunto')
        }),
    )

    # NOVO: Define o valor inicial do campo 'tipo' ao criar uma nova Casa.
    def get_changeform_initial_data(self, request):
        return {'tipo': 'CASA'}


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    """ Admin para o modelo Apartamento. """
    list_display = ('__str__', 'predio', 'andar')
    search_fields = ('numero', 'predio', 'andar')

    # NOVO: Torna o campo 'tipo' imutável.
    readonly_fields = ('tipo',)

    fieldsets = (
        ('Dados Gerais (Endereço)', {
            'fields': ('numero', 'tipo')
        }),
        ('Detalhes do Apartamento', {
            'fields': ('predio', 'andar')
        }),
    )

    # NOVO: Define o valor inicial do campo 'tipo' ao criar um novo Apartamento.
    def get_changeform_initial_data(self, request):
        return {'tipo': 'APARTAMENTO'}


@admin.register(AreaComum)
class AreaComumAdmin(admin.ModelAdmin):
    """ Admin para o modelo AreaComum. """
    list_display = ('__str__', 'local', 'reservavel', 'lotacao')
    list_filter = ('reservavel',)
    search_fields = ('nome', 'local', 'descricao')

    # NOVO: Torna o campo 'tipo' imutável.
    readonly_fields = ('tipo',)

    fieldsets = (
        ('Dados Gerais (Endereço)', {
            'fields': ('numero', 'tipo')
        }),
        ('Detalhes da Área Comum', {
            'fields': ('nome', 'descricao', 'local', 'reservavel', 'lotacao')
        }),
    )

    # NOVO: Define o valor inicial do campo 'tipo' ao criar uma nova Área Comum.
    def get_changeform_initial_data(self, request):
        return {'tipo': 'AREA_COMUM'}