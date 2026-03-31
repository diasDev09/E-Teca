from django.contrib import admin
from .models import Usuario, Livro, Emprestimo

# Customização para o Model Livro
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na listagem
    list_display = ('titulo', 'autor', 'ano_publicado', 'quantidade')
    # Barra de pesquisa (procura por título ou autor)
    search_fields = ('titulo', 'autor')
    # Filtro lateral por categoria
    list_filter = ('categoria',)

# Customização para o Model Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')

# Customização para o Model Emprestimo
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id_emprestimo', 'usuario', 'livro', 'data_emprestimo', 'data_prevista', 'data_devolvido', 'multa')
    # Filtros para ver quem está atrasado ou o que foi devolvido
    list_filter = ('data_emprestimo', 'data_devolvido')
    # Permite clicar no usuário ou livro para ir direto ao cadastro deles
    raw_id_fields = ('usuario', 'livro')