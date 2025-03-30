from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),  # Admin
    path("", auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),  # Página de login
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Página de logout
    path("home/", views.home, name="home"),  # Página inicial após login
    path('avisos/', views.listar_avisos, name='avisos'),
    path('avisos/criar', views.criar_aviso, name='criar_aviso'),
    path('avisos/<int:id>/delete/', views.excluir_aviso, name='excluir_aviso'),
    path('avisos/<int:id>/editar/', views.editar_aviso, name='editar_aviso'),
    path("registros/", views.registros, name="registros"),  # Página de registros
    path("cobranca/", views.cobranca, name="cobranca"),  # Página de cobranças
    path("reuniao/", views.reuniao, name="reuniao"),  # Página de reuniões
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reserva/', views.reserva, name='reserva'),
    path('reserva/criar/', views.criar_reserva, name='criar_reserva'),  # Adiciona a rota para criar_reserva
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/<int:id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:id>/excluir/', views.excluir_usuario, name='excluir_usuario'),
    path("configuracoes/", views.configuracoes, name="configuracoes"),  # Página de configurações
    path('enviar-reuniao/', views.enviar_reuniao, name='enviar_reuniao'),

]
