from django import forms
from .models import Reserva, Aviso
from django import forms
from .models import Reserva
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['area', 'data', 'hora', 'bloco']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        area = cleaned_data.get("area")
        hora = cleaned_data.get("hora")
        bloco = cleaned_data.get("bloco")
        
        if area in ['churrasqueira', 'piscina'] and hora:
            self.add_error('hora', "Churrasqueira e Piscina são reservadas por dia, sem horário específico.")
        elif area == 'salao-de-festa' and not bloco:
            self.add_error('bloco', "Escolha o bloco ao reservar o salão de festas.")
        elif area in ['quadra', 'sala-de-jogos'] and not hora:
            self.add_error('hora', "Selecione um horário ao reservar a quadra ou sala de jogos.")
        
        return cleaned_data


class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['titulo', 'texto']


from django import forms
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        label='Tipo de Usuário',
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecione o tipo de usuário'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Último Nome'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        }
        help_texts = {
            'username': None,  # Remove o help_text
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
        return user