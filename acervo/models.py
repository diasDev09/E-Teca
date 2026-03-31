from django.db import models
from django.utils import timezone
from datetime import timedelta

class Usuario(models.Model):
    nome = models.CharField(max_length=254)
    email = models.EmailField(max_length=254,unique=True)
    telefone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nome
    
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
    id_emprestimo = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_prevista = models.DateTimeField()
    data_devolvido = models.DateTimeField(null=True, blank=True)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.nome}"
    

    