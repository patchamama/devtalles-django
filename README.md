# devtalles-django
devTalles Django. Crea aplicaciones web robustas con Python (notas del curso)

Curso original: https://cursos.devtalles.com/courses/take/django/lessons/64692878-variables

# Sección 1: Introducción al curso

[Instalaciones recomendadas](https://gist.github.com/ricardocuellar/76c13654d9c46cf7bcc92abe3ecbe8a6)


# Sección 2: Fundamentos necesarios de Python


### Funciones de orden superior (High Order Function)

```py
def require_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"

    return wrapper


def admin_dashboard(user):
    return f"Bienvenido al panel, {user}"


auth_view_dashboard = require_auth(admin_dashboard)

print(auth_view_dashboard("Admin"))
print(auth_view_dashboard("Invitado"))
```

### Decoradores

```py
def require_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"

    return wrapper

# auth_view_dashboard = require_auth(admin_dashboard)
# print(auth_view_dashboard("Admin"))

@require_auth
def admin_dashboard(user):
    return f"Bienvenido al panel, {user}"

print(admin_dashboard("Admin"))
print(admin_dashboard("ADMIN"))
```

# Sección 3. Introducción a Django 

En django se usa el modelo MTV y en el mismo donde, en relación al modelo MVC, la vista es el controlador y el template es la vista, más el modelo que es igual. En este modelo el controlador es el encargado de manejar la lógica de la aplicación, interactuar con el modelo y seleccionar la plantilla adecuada para renderizar la respuesta.

### Crear entorno virtual e instalar django

```sh
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar django
pip install django
# o
# pip install "django>=5.2,<6.0"
python3 -m pip install Django

# Guardar dependencias en requirements.txt
pip freeze > requirements.txt
cat requirements.txt

# Crear projecto myproject
django-admin startproject myproject
```

El archivo `asgi.py` en Django sirve como punto de entrada para aplicaciones ASGI (Asynchronous Server Gateway Interface), por ejemplo: HTTP requests síncronos y asíncronos, WebSocket (chat, push notifications), Conexiones de larga duración y Protocolos en tiempo real.

WSGI `wsgi.py` es el estándar de Python para comunicación entre servidores web y aplicaciones web. Es el protocolo síncrono tradicional que Django ha usado desde sus inicios. Por ejemplo: interfaz de servidores web (conecta django con servidores apache, nginx, gunicorn), manejo de requests HTTP síncronos (tradicionales). 


### Ejecutar django

```sh
python3 manage.py runserver

open http://127.0.0.1:8000/
```

### Crear una aplicación

*En el mundo de django las aplicaciones con paquetes o módulos*

```sh
python3 manage.py startapp <app-name>

python3 manage.py runserver
```

### Registrar la aplicación

```py
# myproject/settings.py
INSTALLED_APPS = [
    ...
    'myapp',
]
```

> [!TIP] 
> - Muchas veces se recomienda crear una carpeta llamada `apps` en la raíz del proyecto para agrupar y organizar mejor las aplicaciones, por ejemplo: 
> ```sh
> myproject/
>     apps/
>         myapp/
>         anotherapp/
>     myproject/
> ```
>
> En este caso se debe registrar la aplicación en `settings.py` > `INSTALLED_APPS` como `'apps.myapp'` y además se debe de actualizar el archivo `apps.py` dentro de la aplicación para que el nombre de la aplicación sea correcto, por ejemplo:
>
> ```py
> # apps/myapp/apps.py
> ...
> class MyappConfig(AppConfig):
>     default_auto_field = 'django.db.models.BigAutoField'
>     name = 'apps.myapp' # Antes era 'myapp'
> ```

> [!TIP] 
> - Crear de forma global las carpetas `templates` (\includes) y `static` (y sus subcarpetas css, js e images) en la raíz del proyecto para organizar mejor las plantillas y archivos estáticos.
> - Configurar en `settings.py` las carpetas globales `templates` y `static` para que django las reconozca, por ejemplo:
> ```py
>  TEMPLATES = [
>      {
>          ...
>          'DIRS': [ BASE_DIR / 'templates' ],
>          'APP_DIRS': True,
>          ...
>      },
>  ]
>
> ...
>  STATIC_URL = '/static/'
>  STATICFILES_DIRS = [ BASE_DIR / 'static' ]
> ```


> [!WARNING]
> - No olvidar reiniciar el servidor después de registrar una nueva aplicación.
> - En un inicio es recomendable usar SQLite que es la base de datos por defecto en Django, pero en producción se recomienda usar PostgreSQL.
> - No olvidar instalar el conector de la base de datos que se vaya a usar, por ejemplo, para PostgreSQL: `pip install psycopg2-binary`
> - No olvidar configurar la base de datos en `settings.py` > `DATABASES` según la base de datos que se vaya a usar.
> - No olvidar ejecutar las migraciones después de crear una nueva aplicación o modelo: `python manage.py migrate`  
> - No olvidar crear un superusuario para acceder al panel de administración: `python manage.py createsuperuser`
> - No olvidar registrar los modelos en `admin.py` para que aparezcan en el panel de administración.


### Crear una vista

```py
# myapp/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Hola, mundo!")            
```

### Mapear la vista a una URL

> [!TIP]
> - Es una buena práctica crear un archivo `urls.py` dentro de cada aplicación para manejar las rutas específicas de la aplicación, y luego incluir esas rutas en el archivo `urls.py` del proyecto principal.

```py
# myapp/urls.py
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

```py
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```     

Las views manejan la lógica de la aplicación, interactúan con el modelo y seleccionan la plantilla adecuada para renderizar la respuesta. Las views reciben solicitudes HTTP, procesan los datos necesarios y devuelven respuestas HTTP, estas pueden funcionar usando `funciones` o `clases`.

La función `reverse` se utiliza para obtener la URL correspondiente a una vista basada en su nombre. Esto es útil para evitar hardcoding de URLs en las plantillas y vistas, facilitando el mantenimiento y la refactorización del código.

### Crear una plantilla

_Es una buena práctica crear una carpeta llamada `templates` dentro de la aplicación, y a su vez crear una subcarpeta con el nombre de la aplicación dentro de `templates`._

```html
<!-- myapp/templates/myapp/home.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
</body>
</html> 
```

```py
# myapp/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'myapp/home.html')           
```
### Configurar las plantillas en settings.py

```py
INSTALLED_APPS = [
    ...
    'myapp',
]   
TEMPLATES = [
    {
        ...
        'DIRS': [],
        'APP_DIRS': True, # Busca plantillas en las carpetas 'templates' de cada app
        ...
    },
]
```

Si agregamos plantillas en una carpeta global `templates` en el proyecto, debemos indicarlo en `settings.py`, por ejemplo, sí agregamos una carpeta `templates` en la raíz del proyecto con el archivo `base.html` que contiene la estructura HTML común a todas las páginas, debemos indicarlo en `settings.py`:

```py
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```

# Filtros y etiquetas en plantillas

Los filtros y etiquetas en las plantillas de Django son herramientas poderosas que permiten manipular y presentar datos de manera dinámica. Los filtros se aplican a variables para modificar su salida, mientras que las etiquetas proporcionan funcionalidades más complejas, como estructuras de control y lógica.

Ref: https://docs.djangoproject.com/en/5.2/ref/templates/builtins/

### Filtros comunes

- `{{ variable|upper }}`: Convierte el texto a mayúsculas.
- `{{ variable|lower }}`: Convierte el texto a minúsculas.
- `{{ variable|title }}`: Convierte el texto a formato título (primeras letras en mayúscula).
- `{{ variable|default:"Valor por defecto" }}`: Muestra un valor por defecto si la variable es None o está vacía.
- `{{ variable|length }}`: Devuelve la longitud de una lista, cadena u otro iterable.
- `{{ variable|date:"F j, Y" }}`: Formatea una fecha según el formato especificado.
- `{{ variable|add:5 }}`: Suma 5 al valor numérico de la variable.  

### Etiquetas comunes (tags)

- `{% if condition %} ... {% endif %}`: Estructura condicional.
- `{% for item in list %} ... {% endfor %}`: Bucle para iterar sobre una lista.
- `{% block block_name %} ... {% endblock %}`: Define un bloque de contenido que puede ser sobrescrito en plantillas hijas.
- `{% extends "base.html" %}`: Indica que la plantilla hereda de otra plantilla (base).
- `{% include "partial.html" %}`: Incluye otra plantilla dentro de la actual.   
- `{% url 'view_name' %}`: Genera una URL basada en el nombre de la vista.
- `{% csrf_token %}`: Inserta un token CSRF para proteger formularios contra ataques CSRF.
- `{% load static %}`: Carga el sistema de archivos estáticos para usar archivos CSS, JS, imágenes, etc.
- `{% comment %} ... {% endcomment %}`: Permite agregar comentarios en la plantilla que no se renderizan en el HTML final.
- `{% with variable=value %} ... {% endwith %}`: Asigna un valor a una variable temporal dentro del bloque.
- `{% verbatim %} ... {% endverbatim %}`: Evita que el contenido dentro del bloque sea procesado por el motor de plantillas de Django.
- `{% cycle 'value1' 'value2' %}`: Alterna entre los valores especificados en cada iteración de un bucle.
- `{% regroup list by attribute as grouped_list %}`: Agrupa una lista de objetos por un atributo específico.
- `{% spaceless %} ... {% endspaceless %}`: Elimina espacios en blanco entre etiquetas HTML dentro del bloque.
- `{% firstof var1 var2 "default" %}`: Muestra el primer valor no vacío entre los especificados.
- `{% now "Y-m-d H:i" %}`: Muestra la fecha y hora actual en el formato especificado.
- `{% debug %}`: Muestra información de depuración sobre el contexto actual (útil para desarrollo).
- `{% static "path/to/file" %}`: Genera la URL para un archivo estático.
- `{% load custom_tags %}`: Carga un archivo de etiquetas personalizadas.
- `{% filter filter_name %} ... {% endfilter %}`: Aplica un filtro a todo el contenido dentro del bloque.
- `{% autoescape on/off %} ... {% endautoescape %}`: Controla el autoescape del contenido dentro del bloque.
- `{% include "template.html" %}`: Incluye otra plantilla dentro de la actual.
- `{% blocktrans %} ... {% endblocktrans %}`: Marca un bloque de texto para traducción.<
- `{% url 'view_name' %}`: Genera una URL basada en el nombre de la vista.


Ejemplos:

```html
<p>Nombre en mayúsculas: {{ name | upper }}</p>
<p>Nombre capitalizado: {{ name | title }}</p>
<p>Nombre en minúsculas: {{ name | lower }}</p>
<p>Edad en 5 años: {{ age | add:5 }}</p>
<p>Fecha actual: {{ current_date | date:"F j, Y" }}</p>
<p>Lista de items:</p>
<ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% empty %}
        <li>No hay items disponibles.</li>
    {% endfor %}
</ul>
<p>Condicional:</p>
{% if user.is_authenticated %}
    <p>Bienvenido, {{ user.username }}!</p>
{% else %}
    <p>Por favor, inicia sesión.</p>
{% endif %}
```

### Error 404 personalizada

Para esto se usa un template llamado `404.html` en la carpeta `templates/includes/404.html` y se configura en `settings.py` Debug y Allowed Hosts, y en la vista se lanza el error con `raise Http404("Mensaje de error personalizado")` cuando no se encuentra un recurso.

```py
DEBUG = False
ALLOWED_HOSTS = ['*']  # Permitir todos los hosts para desarrollo, en producción especificar los dominios permitidos
``` 

### Agregar archivos estáticos

Crear una carpeta llamada `static` en la raíz del proyecto y dentro crear subcarpetas para css, js, images, etc.

```sh
mkdir -p static/css static/js static/images
```
En `settings.py` agregar:

```py
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
```
En las plantillas usar:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<script src="{% static 'js/scripts.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

Es importante destacar que Django maneja los archivos estáticos de manera diferente en entornos de desarrollo y producción. Inicialmente es importante especificar `{% load static %}` al inicio de cada plantilla que utilice archivos estáticos para cargar el sistema de archivos estáticos de Django y permitir el uso de la etiqueta `{% static %}` para cargar los archivos estáticos específicos deseados.

Asegurarse que en `settings.py` esté `DEBUG = True` en desarrollo para servir archivos estáticos automáticamente. En producción se debe configurar el servidor web (nginx, apache) para servir estos archivos, y usar `python manage.py collectstatic` para recopilar todos los archivos estáticos en un solo directorio. Adicionalmente la sección "INSTALLED_APPS" debe incluir `'django.contrib.staticfiles'`. En producción, `STATIC_URL` y `STATIC_ROOT` deben estar correctamente configurados para servir los archivos estáticos desde el servidor web.

Se pueden generar archivos estáticos específicos para cada aplicación creando una carpeta `static` dentro de la aplicación, por ejemplo:

```myapp/
    static/
        myapp/
            css/
                myapp_styles.css
            js/
                myapp_scripts.js
            images/
                myapp_logo.png
``` 
Y en la plantilla se referencian como:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'myapp/css/myapp_styles.css' %}">
<script src="{% static 'myapp/js/myapp_scripts.js' %}"></script>
<img src="{% static 'myapp/images/myapp_logo.png' %}" alt="My App Logo">
``` 

También se pueden crear a nivel global en la carpeta `static` en la raíz del proyecto, por ejemplo:

```static/
    css/
        global_styles.css
    js/
        global_scripts.js
    images/
        global_logo.png
```
Y en la plantilla se referencian como:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/global_styles.css' %}">
<script src="{% static 'js/global_scripts.js' %}"></script>
<img src="{% static 'images/global_logo.png' %}" alt="Global Logo">
```

> [!WARNING]
> - No olvidar configurar `STATICFILES_DIRS` en `settings.py` para incluir la carpeta global `static` en la raíz del proyecto, si se usan archivos estáticos a nivel global, ejemplo:  `STATICFILES_DIRS = [ BASE_DIR / 'static' ]`
>
> - No olvidar agregar `'django.contrib.staticfiles'` en `INSTALLED_APPS` en `settings.py` para que Django maneje los archivos estáticos correctamente.
>
> - No olvidar ejecutar `python manage.py collectstatic` en producción para recopilar todos los archivos estáticos en el directorio especificado por `STATIC_ROOT`.
>
> - No se deben crear carpetas `static` dentro de la carpeta `templates`, ya que esto puede causar conflictos y problemas al servir los archivos estáticos. Las carpetas `static` deben estar separadas de las plantillas para mantener una estructura clara y evitar confusiones.
>
> - No olvidar ejecutar el servidor con `python manage.py runserver` para que los cambios en las plantillas y archivos estáticos se reflejen correctamente.

# Sección 7. Modelos y bases de datos

### Interactuar con la base de datos desde el terminal

```sh
sqlite3 db.sqlite3
```

> [!TIP]
> - Recomiendo usar SQLite en desarrollo por su simplicidad, pero en producción usar PostgreSQL.
> - Recomiendo usar la aplicación `Table Plus` o `DB Browser for SQLite` para interactuar con la base de datos SQLite de forma visual. [Table Plus](https://tableplus.com/) (de pago, pero tiene versión gratuita con limitaciones) y [DB Browser for SQLite](https://sqlitebrowser.org/) (gratuito y de código abierto).
> - Si se usa otra base de datos como PostgreSQL o MySQL, se debe usar el cliente correspondiente para interactuar con la base de datos desde el terminal.
> - En PostgreSQL se usa `psql -U username -d dbname` y en MySQL se usa `mysql -u username -p dbname`
> - En SQLite se puede usar el comando `.help` para ver los comandos disponibles.
> - En todos los casos, se puede usar el comando `.exit` para salir del cliente de la base de datos.
> - En SQLite, las tablas creadas por Django tienen el prefijo del nombre de la aplicación, por ejemplo: `myapp_mymodel` para un modelo llamado `MyModel` en una aplicación llamada `myapp`.


### Gestionar base de datos con SQLite desde sql con table Plus

```sql
-- Crear tabla
CREATE TABLE author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    birth_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- En Django sería:  
-- class Author(models.Model):
--     name = models.CharField(max_length=100)
--     bio = models.TextField()
--     birth_date = models.DateField()
--     created_at = models.DateTimeField(auto_now_add=True)
--     updated_at = models.DateTimeField(auto_now=True)

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    published_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- author_id INTEGER,
    -- FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE 
    author_id INTEGER REFERENCES author(id) ON DELETE CASCADE
);  
-- En Django sería: 
-- class Book(models.Model):
--     title = models.CharField(max_length=200)
--     description = models.TextField()
--     published_date = models.DateField()      
--     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
--     created_at = models.DateTimeField(auto_now_add=True)
--     updated_at = models.DateTimeField(auto_now=True)

-- Insertar datos
INSERT INTO author (name, birth_date) VALUES ('James Austen', '1980-01-01');
INSERT INTO book (title, description, published_date, author_id) VALUES ('Orgullo y prejuicio', 'Description de Book 1', '2023-01-01', 1);
-- En Django sería: Author.objects.create(name='James Austen', birth_date='1980-01-01')
-- En Django sería: Book.objects.create(title='Orgullo y prejuicio', description='Description de Book 1', published_date='2023-01-01', author_id=1)

-- Consultar datos
SELECT * FROM author;
-- En Django sería: Author.objects.all()

-- Actualizar datos
UPDATE author SET name='Leonardo Padura' WHERE id=1;
-- En Django sería: Author.objects.filter(id=1).update(name='Leonardo Padura')

-- Asegurar que se borren los libros del autor al borrar el autor (ON DELETE CASCADE)
PRAGMA foreign_keys = ON;  
-- En SQLite las claves foráneas están desactivadas por defecto, se deben activar con PRAGMA
-- En Django siempre están activadas
PRAGMA foreign_keys; -- Verificar que esté activado

-- Eliminar datos
DELETE FROM author WHERE id=1;
DELETE FROM book WHERE id=1;
DROP TABLE author;
DROP TABLE book;
-- En Django sería: Author.objects.filter(id=1).delete()
-- En Django sería: Book.objects.filter(id=1).delete()
-- En Django sería: Author.objects.all().delete()
-- En Django sería: Book.objects.all().delete()

-- Insertar varios registros de una vez
INSERT INTO author (name, birth_date) VALUES 
('J.K. Rowling', '1965-07-31'),
('Gabriel García Márquez', '1985-03-15'),
('Haruki Murakami', '1990-12-10'),
('Isabel Allende', '1975-05-20'),
('Chinua Achebe', '1930-11-16'); 
-- En Django sería: 
-- Author.objects.bulk_create([
--     Author(name='J.K. Rowling', birth_date='1965-07-31'),
--     Author(name='Gabriel García Márquez', birth_date='1985-03-15'),
--     Author(name='Haruki Murakami', birth_date='1990-12-10'),
--     Author(name='Isabel Allende', birth_date='1975-05-20'),
--     Author(name='Chinua Achebe', birth_date='1930-11-16'),
-- ])
INSERT INTO book (title, description, published_date, author_id) VALUES 
('Harry Potter y la piedra filosofal', 'Description de Book 2', '2023-02-01', 2),
('Cien años de soledad', 'Description de Book 3', '2023-03-01', 2),
('Kafka en la orilla', 'Description de Book 4', '2023-04-01', 3),
('La casa de los espíritus', 'Description de Book 5', '2023-05-01', 4),
('El hombre en busca de sentido', 'Description de Book 6', '2023-06-01', 5);
-- En Django sería: 
-- Book.objects.bulk_create([
--     Book(title='Harry Potter y la piedra filosofal', description='Description de Book 2', published_date='2023-02-01', author_id=2),
--     Book(title='Cien años de soledad', description='Description de Book 3', published_date='2023-03-01', author_id=2),
--     Book(title='Kafka en la orilla', description='Description de Book 4', published_date='2023-04-01', author_id=3),
--     Book(title='La casa de los espíritus', description='Description de Book 5', published_date='2023-05-01', author_id=4),
--     Book(title='El hombre en busca de sentido', description='Description de Book 6', published_date='2023-06-01', author_id=5),
-- ])

-- Consultas avanzadas   
SELECT * FROM author;
-- En Django sería: Author.objects.all()
SELECT * FROM book;
-- En Django sería: Book.objects.all()
SELECT * FROM book WHERE author_id=2;
-- En Django sería: Book.objects.filter(author_id=2)
SELECT * FROM book WHERE author_id IN (2, 3);
-- En Django sería: Book.objects.filter(author_id__in=[2, 3])
SELECT * FROM book WHERE author_id BETWEEN 2 AND 3;
-- En Django sería: Book.objects.filter(author_id__range=(2, 3))
SELECT * FROM book WHERE title LIKE '%Book%';
-- En Django sería: Book.objects.filter(title__icontains='Book')
SELECT * FROM book ORDER BY published_date DESC;
-- En Django sería: Book.objects.order_by('-published_date')
SELECT title from book WHERE published_date > '2023-02-15';
-- En Django sería: Book.objects.filter(published_date__gt='2023-02-15')
SELECT * FROM book LIMIT 2 OFFSET 1;
-- En Django sería: Book.objects.all()[1:3]
SELECT COUNT(*) FROM author;
-- En Django sería: Author.objects.count()
SELECT AVG(id) FROM author;
-- En Django sería: Author.objects.aggregate(Avg('id'))
SELECT MAX(id) FROM author;
-- En Django sería: Author.objects.aggregate(Max('id'))
SELECT MIN(id) FROM author;
-- En Django sería: Author.objects.aggregate(Min('id'))
SELECT SUM(id) FROM author;
-- En Django sería: Author.objects.aggregate(Sum('id'))
-- Consultas con subconsultas
SELECT title from book WHERE author_id = (
    SELECT id FROM author WHERE name='Gabriel García Márquez'
);
-- En Django sería: Book.objects.filter(author__name='Gabriel García Márquez').values_list('title', flat=True)
SELECT title from book WHERE author_id = (
    SELECT id FROM author WHERE name='Gabriel García Márquez' or name='J.K. Rowling'
);
-- En Django sería: Book.objects.filter(author__name__in=['Gabriel García Márquez', 'J.K. Rowling']).values_list('title', flat=True)    
-- Simplificar la consulta anterior con IN
SELECT title from book WHERE author_id IN (
    SELECT id FROM author WHERE name='Gabriel García Márquez' or name='J.K. Rowling'
);
-- En Django sería: Book.objects.filter(author__name__in=['Gabriel García Márquez', 'J.K. Rowling']).values_list('title', flat=True)

SELECT author.name, COUNT(book.id) AS book_count
FROM author
LEFT JOIN book ON author.id = book.author_id
GROUP BY author.id, author.name;
-- En Django sería: Author.objects.annotate(book_count=Count('book')).values('name', 'book_count')

SELECT author.name, book.title
FROM author
JOIN book ON author.id = book.author_id
WHERE author.id = 2;
-- En Django sería: Author.objects.filter(id=2).values('name', 'book__title')   

SELECT * FROM books
JOIN author ON books.author_id = author.id
WHERE author.name = 'Gabriel García Márquez';
-- En Django sería: Book.objects.filter(author__name='Gabriel García Márquez')
```

### ORM de Django
 
ORM: Object Relational Mapping (Mapeo Objeto Relacional) es una técnica que permite interactuar con bases de datos relacionales utilizando clases y objetos en un lenguaje de programación en lugar de escribir consultas SQL directamente. Django incluye un ORM potente y fácil de usar que permite definir modelos como clases de Python, y luego realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) utilizando métodos y atributos de estas clases. Al final un ORM traduce estas operaciones en consultas SQL que se ejecutan en la base de datos subyacente.


#### Cómo funciona el ORM de Django

1. **Definición de modelos**: Los modelos se definen como clases de Python que heredan de `django.db.models.Model` y estos representan las tablas de la base de datos. Cada atributo de la clase representa un campo en la tabla de la base de datos y se define utilizando tipos de campo proporcionados por Django (por ejemplo, `CharField`, `TextField`, `DateTimeField`, etc.). Y cada instancia de la clase representa una fila en la tabla. Es decir, como resumen, el ORM hará la traducción entre conceptos de programación orientada a objetos y bases de datos relacionales es la siguiente:

    - Clases u objetos = Tablas
    - Atributos = Columnas o Campos
    - Instancias = Filas o Registros

2. **Migraciones**: Django utiliza un sistema de migraciones para aplicar cambios en los modelos a la base de datos. Cuando se crea o modifica un modelo, se deben crear y aplicar migraciones para reflejar esos cambios en la base de datos.

3. **Consultas**: El ORM permite realizar consultas a la base de datos utilizando una sintaxis de Python en lugar de SQL. Esto incluye operaciones como filtrado, ordenamiento y agregación de datos.

4. **Relaciones**: Django facilita la definición de relaciones entre modelos (por ejemplo, uno a muchos, muchos a muchos) utilizando campos especiales como `ForeignKey` y `ManyToManyField`. Esto permite navegar fácilmente por las relaciones entre los datos.

5. **Consultas avanzadas**: El ORM de Django permite realizar consultas avanzadas utilizando métodos como `annotate()`, `aggregate()`, `prefetch_related()` y `select_related()`, lo que optimiza el rendimiento y reduce la cantidad de consultas a la base de datos.

6. **Administración**: Django incluye un panel de administración automático que se genera a partir de los modelos definidos. Esto permite gestionar los datos de la aplicación sin necesidad de crear interfaces de usuario personalizadas.

7. **Compatibilidad con múltiples bases de datos**: El ORM de Django es compatible con varias bases de datos relacionales, como SQLite, PostgreSQL, MySQL y Oracle. Esto permite cambiar de base de datos sin necesidad de modificar el código de la aplicación.

8. **Seguridad**: El ORM de Django ayuda a prevenir ataques de inyección SQL al utilizar consultas parametrizadas y escapar automáticamente los valores de entrada.

9.  **Facilidad de uso**: El ORM de Django está diseñado para ser fácil de usar y comprender, lo que facilita el desarrollo rápido de aplicaciones web.

10. **Documentación**: Django cuenta con una documentación extensa y bien mantenida que cubre todos los aspectos del ORM, lo que facilita el aprendizaje y la resolución de problemas.

11. **Validación de datos**: El ORM de Django incluye mecanismos de validación de datos integrados que aseguran que los datos almacenados en la base de datos cumplan con las restricciones definidas en los modelos.

12. **Extensibilidad**: El ORM de Django es altamente extensible, lo que permite a los desarrolladores crear campos personalizados, gestores de modelos y otros componentes para adaptarse a las necesidades específicas de su aplicación.

_Como ventaja de usar ORM sobre SQL directo es que el ORM permite escribir código más limpio y mantenible, ya que las consultas se realizan utilizando la sintaxis de Python con objetos en lugar de SQL plano. Además, el ORM facilita la migración entre diferentes sistemas de bases de datos, ya que abstrae las diferencias entre ellos y soporta múltiples backends de bases de datos, el ORM permite una protección básica contra inyecciones SQL y errores._

### Interactuar con la base de datos desde el shell de django

Podemos abrir el shell de django con (y salir con `exit()` ):

```sh
python manage.py shell
``` 
Y dentro del shell podemos interactuar con los modelos y la base de datos, por ejemplo:

```py
from myapp.models import MyModel
# Crear un nuevo objeto
obj = MyModel(field1='value1', field2='value2')
obj.save()
# Consultar objetos
objs = MyModel.objects.all()
for o in objs:
    print(o.field1, o.field2)
# Filtrar objetos
filtered_objs = MyModel.objects.filter(field1='value1')
for o in filtered_objs:
    print(o.field1, o.field2)
# Actualizar un objeto
obj = MyModel.objects.get(id=1)
obj.field1 = 'new_value'
obj.save()
# Eliminar un objeto
obj = MyModel.objects.get(id=1)
obj.delete()
``` 

### Crear un modelo

```py
# myapp/models.py
from django.db import models

class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.field1
```

### Migraciones

```sh
# Crear migraciones
python manage.py makemigrations
# Aplicar migraciones
python manage.py migrate
```
### Registrar el modelo en el admin

```py
# myapp/admin.py
from django.contrib import admin
from .models import MyModel

admin.site.register(MyModel)
```
### Crear un superusuario

```sh
python manage.py createsuperuser
``` 
### Acceder al panel de administración

```sh
python manage.py runserver
```
Abrir en el navegador: http://127.0.0.1:8000/admin/ 
### Consultas básicas con el ORM

```py
from myapp.models import MyModel    
# Crear un nuevo objeto
obj = MyModel(field1='value1', field2='value2')
obj.save()
# Consultar todos los objetos
objs = MyModel.objects.all()
for o in objs:
    print(o.field1, o.field2)
# Filtrar objetos
filtered_objs = MyModel.objects.filter(field1='value1')
for o in filtered_objs:
    print(o.field1, o.field2)
# Obtener un objeto por su ID
obj = MyModel.objects.get(id=1)
print(obj.field1, obj.field2)
# Actualizar un objeto
obj = MyModel.objects.get(id=1)
obj.field1 = 'new_value'
obj.save()
# Eliminar un objeto
obj = MyModel.objects.get(id=1)
obj.delete()
``` 

### Relaciones entre modelos

```py
class Author(models.Model):
    name = models.CharField(max_length=100)     
    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=200)        

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    def __str__(self):
        return self.title
```     

### Consultas con relaciones

```py
# Obtener todos los libros de un autor
author = Author.objects.get(id=1)
books = author.books.all()
for book in books:
    print(book.title)
# Obtener el autor de un libro
book = Book.objects.get(id=1)
print(book.author.name)
``` 

### Eliminar un modelo

```sh
python manage.py makemigrations
python manage.py migrate
```
### Comandos útiles 

```sh
# Ver el estado de las migraciones
python manage.py showmigrations
# Ver las consultas SQL generadas por las migraciones
python manage.py sqlmigrate myapp 0001_initial
# Borrar todas las migraciones y la base de datos (usar con precaución)
rm -rf myapp/migrations
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
``` 

