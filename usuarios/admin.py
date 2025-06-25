from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import Usuario


# Usamos um UserAdmin personalizado para controlar como nosso modelo é exibido.
@admin.register(Usuario)
class UsuarioAdmin(auth_admin.UserAdmin):
    # Campos a serem exibidos na lista de usuários
    list_display = ['cpf', 'is_staff', 'is_active', 'cpf_formatado']

    # Campos pelos quais podemos buscar
    search_fields = ['cpf']

    # Campos pelos quais podemos filtrar
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

    # Campos só de leitura (não editáveis no admin)
    readonly_fields = ('date_joined', 'last_login')

    # Define como os campos são exibidos na página de edição/criação
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Define os campos na tela de criação de um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'password', 'password2'),
        }),
    )

    # Define o campo que será usado para ordenar a lista
    ordering = ['cpf']