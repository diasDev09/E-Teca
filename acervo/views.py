from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Livro, Usuario, Emprestimo

@login_required
def home(request):
    return render(request, 'home.html') # Removida a barra inicial

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça seu login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# LISTAR LIVROS
def listar_livros(request):
    livros = Livro.objects.all()
    return render(request, 'lista_livros.html', {'livros': livros})

# PEGAR LIVRO (EMPRÉSTIMO)
# Removi o usuario_id dos parâmetros para usar o request.user
def pegar_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    usuario = request.user  # Pega o usuário que está logado

    if livro.quantidade > 0:
        try:
            # Garante que as duas operações ocorram juntas ou nenhuma ocorra
            with transaction.atomic():
                data_prevista = timezone.now() + timedelta(days=7)
                
                Emprestimo.objects.create(
                    usuario=usuario,
                    livro=livro,
                    data_prevista=data_prevista
                )
                
                livro.quantidade -= 1
                livro.save()
                
            messages.success(request, f"Empréstimo de '{livro.titulo}' realizado com sucesso!")
        except Exception:
            messages.error(request, "Erro ao processar o empréstimo. Tente novamente.")
    else:
        messages.warning(request, "Este livro não está disponível no momento.")
        
    return redirect('listar_livros')

# DEVOLVER LIVRO E CALCULAR MULTA
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)
    
    if not emprestimo.data_devolvido:
        agora = timezone.now()
        emprestimo.data_devolvido = agora
        
        # Lógica da Multa (R$ 2 por dia de atraso)
        if agora > emprestimo.data_prevista:
            dias_atraso = (agora - emprestimo.data_prevista).days
            emprestimo.multa = dias_atraso * 2.00
        
        # Devolver ao estoque
        emprestimo.livro.quantidade += 1
        emprestimo.livro.save()
        emprestimo.save()

    return render(request, 'recibo.html', {'emprestimo': emprestimo})

def home(request):
    return render(request, 'home.html')