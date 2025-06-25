from django.contrib import admin
from ..models import Pessoa

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    # list_display: Define quais campos do modelo serão exibidos na lista de registros.
    list_display = ('nome_completo', 'cpf', 'email', 'data_nascimento', 'usuario')

    # search_fields: Habilita uma barra de pesquisa e define em quais campos ela irá buscar.
    search_fields = ('nome_completo', 'cpf', 'email')

    # list_filter: Cria uma barra lateral com filtros.
    list_filter = ('data_nascimento',)

    # autocomplete_fields: Melhora a seleção de campos de relacionamento (ForeignKey, ManyToMany, OneToOne).
    # Em vez de um dropdown com todos os usuários (que pode ficar lento),
    # ele cria um campo de busca inteligente. Essencial para 'usuario'.
    autocomplete_fields = ('usuario',)

    # fieldsets: Organiza os campos no formulário de edição em grupos (fieldsets).
    fieldsets = (
        # Primeiro grupo de campos com o título 'Dados Pessoais'
        ('Dados Pessoais', {
            'fields': ('cpf', 'nome_completo', 'data_nascimento', 'email')
        }),
        # Segundo grupo de campos com o título 'Dados de Acesso'
        ('Dados de Acesso', {
            'fields': ('usuario',)
        }),
    )