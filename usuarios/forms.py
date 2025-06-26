from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    # O campo de login padrão do AuthenticationForm se chama 'username'.
    # Vamos apenas modificar seu label e o widget para adicionar classes do Bootstrap.
    username = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu CPF (apenas números)',
            'autofocus': True
        })
    )

    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
        }),
    )