from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

class GestaoPessoaView(LoginRequiredMixin, TemplateView):
    template_name = 'core/gestao_pessoas.html'

class DetalhePessoaView(LoginRequiredMixin, TemplateView):
    template_name = 'core/detalhe_pessoa.html'

class GestaoEnderecosView(LoginRequiredMixin, TemplateView):
    template_name = 'core/gestao_enderecos.html'

class DetalheEnderecoView(LoginRequiredMixin, TemplateView):
    template_name = 'core/detalhe_endereco.html'