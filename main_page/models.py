from django.db import models
from django.contrib.postgres.fields import ArrayField
from environs import Env

class Genere (models.Model):
    GENRE_CHOICES = [
        ('comedy', 'Комедия'),
        ('fantasy', 'Фентези'),
        ('fantastic', 'Фантастика'),
        ('horror', 'Ужасы'),
        ('detective', 'Детектив'),
        # добавьте больше жанров по необходимости
    ]
    genere = models.CharField(max_length=20, choices=GENRE_CHOICES)
    def __str__(self):
        return self.genere

class NewFilm(models.Model):

    title = models.CharField(max_length=255, default='Default value')
    description = models.TextField()
    video = models.FileField(upload_to='movies/')
    image = models.FileField(upload_to='baners/')
    genre = models.ManyToManyField(Genere)
    def __str__(self):
        return self.title


class AllFilms (models.Model):

    title = models.CharField(max_length=255, default='default value')
    description = models.TextField()
    video = models.CharField(max_length=400)
    image = models.CharField(max_length=400)
    genre = models.ManyToManyField(Genere)
    env = Env()
    env.read_env()
    
    def __str__(self):
        return self.title
    @property
    def video_url(self):
        if self.video.startswith("http://") or self.video.startswith("https://"):
            return self.video
        return f'{self.env('STORAGE_LINK')+self.video}'
    @property
    def image_url(self):
        if self.image.startswith("http://") or self.image.startswith("https://"):
            return self.image
        return f'{self.env('STORAGE_LINK')+self.image}'

class Comment(models.Model):
    film = models.ForeignKey(AllFilms, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.id} on {self.film}'

class OkkoFilms(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1200)
    image_url = models.URLField(max_length=500)
    trailer_url = models.URLField(max_length=500, blank=True, null=True)
    def __str__(self) -> str:
        return self.title


# Create your models here.

