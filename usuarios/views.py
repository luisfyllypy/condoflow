from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import CustomAuthenticationForm

class LoginView(AuthLoginView):
    template_name = 'usuarios/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True # Redireciona usuários já logados