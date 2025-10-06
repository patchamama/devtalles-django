from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Book
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get('query_search', None)  # Obtener el parámetro de búsqueda 'query_search' de la URL si está presente
        date_start = request.GET.get('date_start', None)  # Obtener el parámetro de fecha de inicio 'date_start' de la URL si está presente
        date_end = request.GET.get('date_end', None)  # Obtener el parámetro de fecha de fin 'date_end' de la URL si está presente
        if date_start and date_end:
            books = books.filter(publication_date__range=[date_start, date_end])
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )  # Filtrar libros por título que contenga la cadena de búsqueda (case-insensitive)
            
        paginator = Paginator(books, 5)  # Mostrar 5 libros por página
        page_number = request.GET.get('page')  # Obtener el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtener los libros para la página actual y manejar errores automáticamente

        query_params = request.GET.copy()  # Copiar los parámetros GET de la solicitud en un diccionario mutable
        if 'page' in query_params:
            del query_params['page']  # Eliminar el parámetro 'page' para mantener otros parámetros en la paginación
            # query_params.pop("page", None)  # Eliminar el parámetro 'page' para mantener otros parámetros en la paginación
        query_string = query_params.urlencode()  # Codificar los parámetros restantes en una cadena de consulta
        
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
             "page_obj": page_obj,
             "query": query if query else "",
             "query_string": query_string,
        })
    except Exception as e:
        return HttpResponseNotFound(f"Error loading page: {e}")