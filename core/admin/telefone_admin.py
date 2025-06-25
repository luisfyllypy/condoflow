from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from ..models import Telefone

class TelefoneAdminForm(forms.ModelForm):
    """
    Formulário personalizado para o admin de Telefone, com validação da regra de negócio.
    """
    class Meta:
        model = Telefone
        fields = '__all__'

    def clean(self):
        # O método clean() é onde fazemos validações que envolvem múltiplos campos.
        cleaned_data = super().clean()
        pessoa = cleaned_data.get('pessoa')
        endereco = cleaned_data.get('endereco')

        # Regra 1: Ambos não podem estar preenchidos ao mesmo tempo.
        if pessoa and endereco:
            raise ValidationError(
                "Um telefone deve estar associado a uma Pessoa OU a um Endereço, mas não a ambos."
            )

        # Regra 2: Pelo menos um dos dois deve estar preenchido.
        if not pessoa and not endereco:
            raise ValidationError(
                "Um telefone precisa estar associado a uma Pessoa ou a um Endereço."
            )

        return cleaned_data


@admin.register(Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    """
    Configurações de administração para o modelo Telefone.
    """
    # Usa o formulário personalizado que criamos acima para aplicar nossas validações.
    form = TelefoneAdminForm

    # Mostra os campos mais relevantes na lista. O __str__ do modelo já é bom.
    list_display = ('__str__', 'tipo', 'pessoa', 'endereco')

    # Permite filtrar os telefones por tipo.
    list_filter = ('tipo',)

    # Permite buscar um telefone pelo número ou pelo nome da pessoa associada.
    # Note a sintaxe 'pessoa__nome_completo' para buscar em um campo de um modelo relacionado.
    search_fields = ('numero', 'pessoa__nome_completo')

    # Essencial para campos ForeignKey com muitos registros. Melhora a usabilidade.
    autocomplete_fields = ('pessoa', 'endereco')