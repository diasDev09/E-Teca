from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro, Usuario, Emprestimo
from django.utils import timezone
from datetime import timedelta

# LISTAR LIVROS
def listar_livros(request):
    livros = Livro.objects.all()
    return render(request, 'livraria/lista_livros.html', {'livros': livros})

# PEGAR LIVRO (EMPRÉSTIMO)
def pegar_livro(request, livro_id, usuario_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if livro.quantidade > 0:
        # Lógica do script: 7 dias de prazo
        data_prevista = timezone.now() + timedelta(days=7)
        
        Emprestimo.objects.create(
            usuario=usuario,
            livro=livro,
            data_prevista=data_prevista
        )
        
        # Diminuir estoque
        livro.quantidade -= 1
        livro.save()
        
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

    return render(request, 'livraria/recibo.html', {'emprestimo': emprestimo})