from django.db import models
from django.contrib.auth.models import User # Importação essencial para o login
from django.utils import timezone

class Livro(models.Model):
    titulo = models.CharField(max_length=254)
    autor = models.CharField(max_length=254)
    ano_publicado = models.IntegerField()
    categoria = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

class Emprestimo(models.Model):
    # Usamos a chave primária automática do Django ou mantemos o BigAutoField
    id_emprestimo = models.BigAutoField(primary_key=True)
    
    # CORREÇÃO: Agora aponta para o 'User' do Django, permitindo usar request.user
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emprestimos')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='historico')
    
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_prevista = models.DateTimeField()
    data_devolvido = models.DateTimeField(null=True, blank=True)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.username}"

# OPCIONAL: Se você quiser guardar o telefone, transforme o Usuario em um Perfil
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"