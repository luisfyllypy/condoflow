from django.urls import path
from .views import HomeView, GestaoPessoaView, DetalhePessoaView, GestaoEnderecosView, DetalheEnderecoView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('gestao_pessoas/', GestaoPessoaView.as_view(), name='gestao_pessoas'),
    path('detalhe_pessoa/', DetalhePessoaView.as_view(), name='detalhe_pessoa'),
    path('gestao_enderecos/', GestaoEnderecosView.as_view(), name='gestao_enderecos'),
    path('detalhe_endereco/', DetalheEnderecoView.as_view(), name='detalhe_endereco'),
]