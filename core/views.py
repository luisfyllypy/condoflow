from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ReservaForm, AvisoForm
from .models import Reserva, Aviso
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm


# View para criar um aviso (acesso restrito a administradores)
@login_required
def criar_aviso(request):
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('avisos')
    else:
        form = AvisoForm()
    return render(request, 'core/criar_aviso.html', {'form': form})

# View para listar avisos
@login_required
def listar_avisos(request):
    avisos = Aviso.objects.all() 
    return render(request, 'core/avisos.html', {'avisos': avisos})

# View para editar um aviso
@login_required
def editar_aviso(request, id):
    aviso = get_object_or_404(Aviso, id=id)
    
    if request.method == 'POST':
        form = AvisoForm(request.POST, instance=aviso)
        if form.is_valid():
            form.save()
            return redirect('avisos')  # Redireciona após editar
    else:
        form = AvisoForm(instance=aviso)  # Preenche o formulário com os dados existentes

    return render(request, 'core/editar_aviso.html', {'form': form, 'aviso': aviso})

# View para confirmar a exclusão de um aviso
@login_required
def excluir_aviso(request, id):
    aviso = get_object_or_404(Aviso, id=id)
    if request.method == 'POST':
        aviso.delete()
        return redirect('avisos')  # Redireciona após a exclusão
    return render(request, 'core/confirm_delete.html', {'aviso': aviso})

""" RESERVAS """
def listar_reservas(request):
    reservas = Reserva.objects.all()
    reservas_por_area = {
        'Churrasqueira': reservas.filter(area='churrasqueira'),
        'Piscina': reservas.filter(area='piscina'),
        'Quadra de Esportes': reservas.filter(area='quadra'),
        'Sala de Jogos': reservas.filter(area='sala-de-jogos'),  # Corrigido o nome
        'Salão de Festas': reservas.filter(area='salao-de-festa'),  # Corrigido o nome
        
    }
    return render(request, 'core/reservas.html', {'reservas_por_area': reservas_por_area})

def reserva(request):
    if request.method == 'POST':
        # Lógica para criar uma nova reserva
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_reservas')  # Certifique-se de que esse nome de URL existe
    else:
        form = ReservaForm()

    return render(request, 'core/reserva_form.html', {'form': form})




# View para criar uma nova reserva
@login_required
def criar_reserva(request):
    if request.method == 'POST':
        area = request.POST.get('area')
        data = request.POST.get('data')
        hora = request.POST.get('hora')

        # Obter o nome do usuário logado
        usuario_nome = request.user.username

        # Verifica se a área e a data foram escolhidas
        if not area or not data:
            messages.error(request, "Por favor, selecione uma área e uma data.")
            return render(request, 'core/criar_reserva.html')

        # Se a hora for um campo opcional, assegure-se de que não está vazio
        if not hora:  # Caso a hora não tenha sido selecionada
            hora = None  # Ou defina um valor padrão se necessário

        # Verifica se já existe uma reserva para a data e área selecionadas
        if Reserva.objects.filter(area=area, data=data, hora=hora).exists():
            messages.error(request, "Já existe uma reserva para este horário.")
            return render(request, 'core/criar_reserva.html')

        # Se não existir reserva, continue com a criação
        reserva = Reserva(area=area, data=data, hora=hora, usuario_nome=usuario_nome)
        reserva.save()
        messages.success(request, "Reserva criada com sucesso!")
        return redirect('reserva')  # Redirecione para a lista de reservas

    return render(request, 'core/criar_reserva.html')


# View para editar uma reserva existente
@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            area = reserva.area
            data_reserva = reserva.data

            # Verifica se a alteração respeita os limites de reserva
            reservas_no_dia = Reserva.objects.filter(area=area, data=data_reserva).exclude(id=reserva.id)
            if area in ['churrasqueira', 'piscina'] and reservas_no_dia.count() >= 10:
                messages.error(request, "Limite de 10 reservas por dia atingido para esta área.")
            elif area in ['quadra', 'sala de jogos'] and reservas_no_dia.count() >= 2:
                messages.error(request, "Limite de 2 reservas de 1 hora atingido para esta área.")
            elif area == 'salão de festas' and reservas_no_dia.count() >= 5:
                messages.error(request, "Limite de 5 reservas para o salão de festas atingido.")
            else:
                reserva.save()
                messages.success(request, "Reserva atualizada com sucesso!")
                return redirect('listar_reservas')
    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'core/editar_reserva.html', {'form': form, 'reserva': reserva})

# View para excluir uma reserva existente
@login_required
def excluir_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva excluída com sucesso!")
        return redirect('listar_reservas')
    
    return render(request, 'core/confirmar_exclusao_reserva.html', {'reserva': reserva})  
""" RESERVAS """

# Views para renderizar páginas principais
@login_required
def home(request):
    return render(request, "core/home.html")

@login_required
def avisos(request):
    return listar_avisos(request)  # Reutiliza a função listar_avisos

@login_required
def reserva(request):
    return listar_reservas(request)  # Reutiliza a função listar_avisos


from django.contrib.auth.models import User

@login_required
def registros(request):
    usuarios = User.objects.all()
    return render(request, 'core/registros.html', {'usuarios': usuarios})

@login_required
def cobranca(request):
    return render(request, "core/cobranca.html")

@login_required
def reuniao(request):
    return render(request, "core/reuniao.html")

@login_required
def configuracoes(request):
    return render(request, "core/configuracoes.html")

def login(request):
    return render(request, "core/login.html")


from django.contrib.auth.models import User
from .forms import UserForm

# View para criar um usuário

@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registros')
    else:
        form = UserForm()
    return render(request, 'core/criar_usuario.html', {'form': form})

# View para listar usuários
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/listar_usuarios.html', {'usuarios': usuarios})


# View para editar um usuário
@login_required
def editar_usuario(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('registros')
    else:
        form = UserForm(instance=user)
    return render(request, 'core/editar_usuario.html', {'form': form})

# View para excluir um usuário
@login_required
def excluir_usuario(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('registros')
    return render(request, 'core/excluir_usuario.html', {'user': user})

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

@csrf_exempt
def enviar_reuniao(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        assunto = data.get('assunto')
        local = data.get('local')
        data_reuniao = data.get('data')
        urgencia = data.get('urgencia')
        descricao = data.get('descricao')
        mensagem = data.get('mensagem')
        destinatarios = data.get('destinatarios')

        # Obter os e-mails dos destinatários
        if destinatarios == 'funcionarios':
            emails = User.objects.filter(profile__user_type='F').values_list('email', flat=True)
        elif destinatarios == 'moradores':
            emails = User.objects.filter(profile__user_type='M').values_list('email', flat=True)
        else:  # todos
            emails = User.objects.all().values_list('email', flat=True)

        # Enviar e-mail
        send_mail(
            assunto,
            f'Local: {local}\nData: {data_reuniao}\nUrgência: {urgencia}\nDescrição: {descricao}\nMensagem: {mensagem}',
            'ainnguttoo@gmail.com',
            emails,
            fail_silently=False,
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})