import random
import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete


class Livro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    espirito = models.CharField(max_length=100)
    editora = models.CharField(max_length=100)
    ano_public = models.CharField(max_length=10)
    def _gerar_codigo_aleatorio(self):
        return str(random.randint(10000, 99999))

    def __str__(self):
        return self.titulo

def gerar_nome_arquivo(instance, filename):
    # Obter a extensão do arquivo original
    ext = filename.split('.')[-1]
    # Gerar um nome único baseado no nome do cliente e extensão do arquivo
    novo_nome = f"{instance.nome.replace(' ', '_').lower()}_img.{ext}"
    # Retornar o caminho completo para o upload
    return os.path.join('clientes/', novo_nome)

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    email = models.EmailField()
    foto = models.ImageField(upload_to=gerar_nome_arquivo, null=True, blank=True)

    def __str__(self):
        return self.nome
        
##### FUNCOES GERAIS ####
def excluir_arquivo_foto(sender, instance, **kwargs):
    # Verifique se o arquivo existe e exclua-o
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

def atualizar_arquivo_foto(sender, instance, **kwargs):
    # Verifique se uma nova foto foi enviada
    if instance.pk:
        try:
            old_instance = Cliente.objects.get(pk=instance.pk)
            if old_instance.foto and old_instance.foto != instance.foto:
                # Exclua a foto antiga
                old_instance.foto.delete(save=False)
        except Cliente.DoesNotExist:
            pass
# Conecte os sinais após as funções serem definidas
post_delete.connect(excluir_arquivo_foto, sender=Cliente)
pre_save.connect(atualizar_arquivo_foto, sender=Cliente)

class Emprestimo(models.Model):
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Empréstimo para {self.cliente.nome} em {self.data_emprestimo}"

class Venda(models.Model):
    data_venda = models.DateTimeField(auto_now_add=True)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    preco = models.FloatField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venda de {self.livro.titulo} em {self.data_venda}"

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Estoque(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='estoques')
    quantidade = models.PositiveIntegerField()
    estante = models.CharField(max_length=50)
    prateleira = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.livro.titulo} - Quantidade: {self.quantidade}"
