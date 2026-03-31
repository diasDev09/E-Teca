from django import forms
from .models import Usuario, Livro, Emprestimo

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'telefone']

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'