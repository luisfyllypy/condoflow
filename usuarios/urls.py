from django.urls import path
from .views import LoginView
from django.contrib.auth import views


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
]