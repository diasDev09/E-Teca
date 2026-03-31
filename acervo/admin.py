from django.contrib import admin
# Remova 'Usuario' da lista abaixo, pois ele não existe mais no models.py
from .models import Livro, Emprestimo, Perfil 

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'quantidade', 'categoria')
    search_fields = ('titulo', 'autor')

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_emprestimo', 'data_prevista')
    list_filter = ('data_emprestimo', 'data_prevista')

# Se você criou o model Perfil no models.py, registre-o aqui:
admin.site.register(Perfil)