from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Registrar o modelo Livro
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editora', 'ano_public')
    list_filter = ('autor', 'editora')
    search_fields = ('titulo', 'autor')
    def save_model(self, request, obj, form, change):
        # Verifica se é um novo livro sendo criado (não uma edição)
        if not obj.pk:
            obj.save()  # Salva o livro para obter o ID gerado automaticamente
            # Agora podemos exibir o código gerado
            self.message_user(request, f'O código do livro gerado é: {obj.exemplar.codigo}', level='SUCCESS')
        else:
            obj.save()

# Registrar o modelo Exemplar
@admin.register(Exemplar)
class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'livro', 'estante', 'prateleira', 'localizacao')
    list_filter = ('estante', 'prateleira', 'livro__titulo')
    search_fields = ('codigo', 'livro__titulo')

# Registrar o modelo Emprestimo
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_emprestimo', 'data_devolucao')
    list_filter = ('cliente__nome', 'data_emprestimo', 'data_devolucao')
    search_fields = ('cliente__nome',)

# Registrar o modelo Venda
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'exemplar', 'data_venda', 'preco')
    list_filter = ('cliente__nome', 'data_venda')
    search_fields = ('cliente__nome', 'exemplar__livro__titulo')

# Registrar o modelo Funcionario
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'email')
    list_filter = ('cargo',)
    search_fields = ('nome', 'cargo')

# Registrar o modelo Estoque
@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('livro', 'quantidade')
    list_filter = ('livro__titulo',)
    search_fields = ('livro__titulo',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('imagem_preview', 'nome', 'endereco', 'email')
    search_fields = ('nome', 'endereco', 'email')

    def imagem_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="height: 50px; width: 50px;">', obj.foto.url)
        return '(Sem foto)'

    imagem_preview.short_description = 'Foto'