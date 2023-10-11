from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PostsPublicados(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publicado')


class ComentariosPublicados(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='aprovado')


class Postagem(models.Model):
    objects = models.Manager()
    publicados = PostsPublicados()
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    corpo = models.TextField()
    publicado = models.DateTimeField(default=timezone.now)
    criado = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default='rascunho')
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_autor')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publicado']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    postagem = models.ForeignKey(
        Postagem, on_delete=models.CASCADE, related_name='comentarios')
    publicados = ComentariosPublicados()
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=100)
    texto = models.TextField()
    criado = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
    )
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        ordering = ['-criado']

    def __str__(self):
        return f'Comentário por {self.nome} em {self.postagem}'
