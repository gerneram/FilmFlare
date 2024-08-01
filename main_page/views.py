from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from .models import NewFilm
from .serializers import TextItemSerializer
from django.shortcuts import render
from .models import NewFilm,AllFilms,Comment



class TextItemCreate(generics.CreateAPIView):
    queryset = NewFilm.objects.all()
    serializer_class = TextItemSerializer

class TextItemDelete(generics.DestroyAPIView):
    queryset = NewFilm.objects.all()
    serializer_class = TextItemSerializer


def index(request):
    films = NewFilm.objects.all()
    return render(request, 'main_page/base.html', {'films': films})


def get_movies(request):
    genre_id = request.GET.get('genre')

    if genre_id and genre_id.isnumeric() and genre_id != 'All':
        genre_id = int(genre_id)  # Преобразование в целое число
        movies = AllFilms.objects.filter(genre__id=genre_id)
    else:
        movies = AllFilms.objects.all()

    movie_data = []
    for movie in movies:
        movie_data.append({
            'id': movie.id,
            'title': movie.title,
            'image_url': movie.image_url,
            'trailer_url': movie.video_url,
        })

    return JsonResponse({"movies": movie_data})


def add_comment(request, film_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        film = AllFilms.objects.get(pk=film_id)
        Comment.objects.create(film=film, text=text)
        return JsonResponse({"success": True})

#def get_comments(request, film_id):
#    comments = Comment.objects.filter(film__id=film_id).order_by('-created_at')
#    comments_data = [{"id": comment.id, "text": comment.text, "created_at": comment.created_at} for comment in comments]
#    return JsonResponse({"comments": comments_data})

def get_comments(request, film_id):
    comments = Comment.objects.filter(film__id=film_id).values('id', 'text', 'created_at')  # Или любые другие поля, которые вы хотите отправить
    comments_list = list(comments)
    return JsonResponse({'comments': comments_list})
