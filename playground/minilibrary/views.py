from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Book
from django.db.models import Q

# Create your views here.
def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get('query_search', None)  # Obtener el parámetro de búsqueda 'query_search' de la URL si está presente
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )  # Filtrar libros por título que contenga la cadena de búsqueda (case-insensitive)
        # author_id = request.GET.get('author', None)  # Obtener el parámetro author_id de la URL si está presente
        # genre_id = request.GET.get('genre', None)  # Obtener el parámetro genre_id de la URL si está presente
        # if author_id:
        #     books = books.filter(author_id=author_id)  # Filtrar libros por el ID del autor si se proporciona: http://localhost:8000/minilibrary/?author=6
        # if genre_id:
        #     books = books.filter(genres__id=genre_id)  # Filtrar libros por el ID del género si se proporciona
        return render(request, 'minilibrary/minilibrary.html', {
            #  "text": "Bienvenido a la Mini Biblioteca",
            #  "name": "Ricardo",
            #  "author": author_id if author_id else "Invitado",
             "books": books,
             "query": query if query else "",
        })
    except Exception as e:
        return HttpResponseNotFound(f"Error loading page: {e}")