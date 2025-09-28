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

*Makemigrations* y *migrate* son comandos de Django que se utilizan para gestionar los cambios en la estructura de la base de datos a lo largo del ciclo de vida de una aplicación web. Estos comandos trabajan en conjunto para crear, aplicar y revertir migraciones, que son archivos que describen los cambios en los modelos de Django y cómo deben reflejarse en la base de datos. *Makemigrations* crea los archivos de migración basados en los cambios realizados en los modelos, mientras que *migrate* aplica esos cambios a la base de datos. 

Para ver sí hay alguna migración pendiente se puede usar el comando `python manage.py showmigrations` que muestra una lista de todas las migraciones disponibles y su estado (aplicadas o pendientes).

Una vez que se han creado las migraciones con `makemigrations`, se pueden aplicar a la base de datos utilizando el comando `migrate`. Este comando ejecuta las migraciones pendientes en el orden correcto, asegurando que la estructura de la base de datos esté sincronizada con los modelos de Django, así que es importante ejecutar `migrate` después de `makemigrations` para que los cambios en los modelos se reflejen en la base de datos cuando se realizan cambios en los modelos.

### Django shell

El shell de Django es una herramienta interactiva que permite a los desarrolladores ejecutar código Python en el contexto de una aplicación Django. Proporciona un entorno para probar y depurar código, interactuar con modelos y bases de datos, y realizar tareas administrativas sin necesidad de crear scripts o interfaces de usuario.

Para acceder al shell de Django, se puede utilizar el siguiente comando (para salir es con exit() o Ctrl+D):

```sh
python3 manage.py shell
```

Recomendable instalar IPython para una mejor experiencia interactiva en el shell de Django:

```sh
pip install ipython  # Opcional, para una mejor experiencia interactiva
```

Esto abrirá un intérprete de Python con el entorno de Django cargado, lo que permite a los desarrolladores interactuar con sus modelos y realizar consultas a la base de datos de manera sencilla usando python y el ORM de Django, ejemplo:

```py
from minilibrary.models import Book, Author
# Crear un nuevo objeto
orwell = Author.objects.create(name='George Orwell', birth_date='1903-06-25')
orwell.save()
book = Book.objects.create(title='1984', published_date='1949-06-08', author=orwell, pages=328, isbn='9780451524935')
# book.save() # no es necesario pues con create ya se crea y guarda en la base de datos
# Otra forma de crear un objeto, en este caso se crea una instancia con valores en el constructor y luego se guarda
author = Author(name='J.K. Rowling', birth_date='1965-07-31')
author.name = 'J.K. Rowling' # Asignar el nombre del autor nuevo, permitiendo modificaciones antes de guardar
author.name = author.name.upper()  # Convertir el nombre a mayúsculas
author.save() # Guardar el autor en la base de datos
book = Book(title='Harry Potter and the Philosopher\'s Stone', published_date='1997-06-26', author=author, pages=223, isbn='9780747532699')
book.save()

cuellar = Book.objects.get(title='La ciudad y los perros') # Obtener un libro por su título después de buscarlo en la base de datos
rowling = Author.objects.get(name='J.K. Rowling') # Obtener un autor por su nombre después de buscarlo en la base de datos

# Crear varios objetos a la vez para el autor Cuéllar almacenado en la variable mario.
Book.objects.bulk_create([  # Insertar varios registros de una vez
    Book(title='El amor en los tiempos del cólera', published_date='1985-03-05', author=rowling, pages=348, isbn='9780307389732'),
    Book(title='La casa verde', published_date='1966-01-01', author=rowling, pages=400, isbn='9780141187690'),
    Book(title='Conversación en La Catedral', published_date='1969-01-01', author=rowling, pages=600, isbn='9780141187706'),
])

# Insertar muchos objetos de una vez y medir el tiempo que tarda
import time
start = time.time()
books = []
for i in range(1000):
    books.append(Book(title=f'Book {i}', published_date='2023-01-01', author=rowling, pages=100 + i, isbn=f'9780000000{i}'))
    # De esta otra forma tardaría mucho pues cada vez que se hace un book.save() se hace una consulta a la base de datos:
    # book = Book(title=f'Book {i}', published_date='2023-01-01', author=rowling, pages=100 + i, isbn=f'9780000000{i}')
    # book.save()  # Guardar cada libro individualmente (más lento)
Book.objects.bulk_create(books)  # Insertar 1000 libros de una vez
end = time.time()
print(f'Tiempo para insertar 1000 libros: {end - start:.2f} segundos')

# Crear registros de forma segura con get_or_create
# Esto evita crear registros duplicados si ya existen:
mario = Author.objects.get_or_create(name='Mario Vargas Llosa', defaults={'birth_date': '1936-03-28'})
ricardo = Author.objects.get_or_create(name='Ricardo Cuéllar', defaults={'birth_date': '1970-01-01'}) # Si el autor ya existe, no se crea uno nuevo, created será False sí no se creó

# Consultar objetos (Consultas básicas con el ORM)
books = Book.objects.all() # Obtener todos los objetos o registros (Select * from book)
for b in books:
    print(b.title, b.author.name)
# Obtener un objeto por su ID
book = Book.objects.get(id=1)
book = Book.objects.get(id__exact=1) # Otra forma de obtener un objeto por su ID (especificando el operador exact) (select * from book where id = 1 limit 1)
print(book.title, book.author.name)
book = Book.objects.get(title='1984') 
print(book.title, book.author.name)
## Hacer búsqueda con campo de búsqueda (field lookup):
## __exact: Igual a (case-sensitive) y es lo mismo que __exact (WHERE field = value)
## __iexact: Igual a (case-insensitive) y es lo mismo que __iexact (WHERE field ILIKE value)
## __contains: Contiene (case-insensitive), da igual __contains como __icontains (LIKE %value%)
## __gt: Mayor que, greater than (field > %value%) field__gt=value
## __gte: Mayor o igual que, greater and equal than (field >= %value%) field__gte=value
## __lt: Menor que, less than (field < %value%) field__lt=value
## __lte: Menor o igual que, less and equal than (field <= %value%) field__lte=value
## __startswith: Empieza con (case-insensitive) y es lo mismo que __istartswith (LIKE value%)
## __endswith: Termina con (case-insensitive) y es lo mismo que __iendswith (LIKE %value)
## __in: En una lista de valores (field IN (value1, value2, ...)) field__in=[value1, value2, ...]
## __range: En un rango de valores (field BETWEEN value1 AND value2) field__range=(value1, value2)
## __isnull: Es nulo o no es nulo (field IS NULL o field IS NOT NULL) field__isnull=True o field__isnull=False
## __regex: Coincide con una expresión regular (field REGEXP 'pattern') field__regex='pattern'
## __iregex: Coincide con una expresión regular (case-insensitive) (field REGEXP 'pattern') field__iregex='pattern'
## __date: Convierte el campo en una fecha específica, por ejemplo, un string a fecha (field = 'YYYY-MM-DD') field__date='YYYY-MM-DD', 
## __year: Coincide con un año específico (field = YYYY) field__year=YYYY
## __month: Coincide con un mes específico (field = MM) field__month=MM
## __day: Coincide con un día específico (field = DD) field__day=DD
## __week_day: Coincide con un día de la semana específico (field = 1-7) field__week_day=1-7 (1=Domingo, 2=Lunes, ..., 7=Sábado)
## __time: Coincide con una hora específica (field = 'HH:MM:SS') field__time='HH:MM:SS'
## __hour: Coincide con una hora específica (field = HH) field__hour=HH
## __minute: Coincide con un minuto específico (    field = MM) field__minute=MM
## __second: Coincide con un segundo específico (field = SS) field__second=SS
## __search: Búsqueda de texto completo (field MATCH 'value') field
book = Book.objects.filter(title__exact='catedral') # Búsqueda case-sensitive, exacto, en este caso busca 'Catedral' pero no 'catedral' ni 'CATEDRAL'
book = Book.objects.filter(title__iexact='catedral') # Búsqueda case-insensitive, ignora mayúscula y minúsculas, en este caso busca 'Catedral' o 'catedral' o 'CATEDRAL' pero con el valor exacto
book = Book.objects.filter(title__contains='Catedral') # Búsqueda case-insensitive (da igual __contains como __icontains), en este caso busca '%Catedral%' pero no 'catedral' ni 'CATEDRAL' (WHERE "minilibrary_book"."title" LIKE %catedral% ESCAPE '\')
book = Book.objects.filter(title__icontains='catedral').exists() # Devuelve sí existe algún libro que contenga 'catedral' (case-insensitive)
book = Book.objects.filter(title__startswith='La') # Búsqueda case-insensitive, en este caso busca 'La%' y da igual sí empieza como 'la%' ni 'LA%' (LIKE conv%)
book = Book.objects.filter(id__gt=5) # Búsqueda mayor que
book = Book.objects.filter(pages__gte=5) # Búsqueda mayor o igual que, pages >= 5
book = Book.objects.filter(id__in=[1, 2, 3]) # Búsqueda en una lista de valores
book = Book.objects.filter(id__in=[1, 2, 3, 4], title__icontains='catedral') # Búsqueda en una lista de valores (where id in (1, 2, 3, 4) and title like %catedral%)
print(book[0].title, book[0].author.name, str(book.query)) # Obtener el primer libro que cumple con el filtro y ver el SQL generado por el ORM
# Filtrando por fechas y rango de fechas
books = Book.objects.filter(published_date__year=2023) # Búsqueda por año (WHERE "minilibrary_book"."published_date" BETWEEN 2023-01-01 AND 2023-12-31) 
from datetime import date
books = Book.objects.filter(published_date=date(2000, 1, 1)) 
books = Book.objects.filter(published_date__lte=date(2000, 1, 1)) 
books_in_range = Book.objects.filter(published_date__range=['2000-01-01', '2023-12-31']) # Búsqueda en un rango de fechas (where published_date between '2000-01-01' and '2023-12-31')
for b in books_in_range:
    print(b.title, b.published_date)
print(books_in_range.query) # Ver el SQL generado por el ORM
# Encadenamiento de filtros (AND) se hace con varios filter() uno detrás de otro
books = Book.objects.filter(published_date__year=2023).filter(author__name__icontains='Rowling') # Búsqueda por año y autor (where published_date between '
# Exclusión de registros (AND NOT)
books_not_2023 = Book.objects.exclude(published_date__year=2023) # Búsqueda por año excluyendo 2023 (where published_date not between '2023-01-01' and '2023-12-31')
for b in books_not_2023:
    print(b.title, b.published_date)
books = Book.objects.filter(published_date__year=2023).filter(author__name__icontains='Rowling').exclude(title__icontains='Harry') # Búsqueda por año y autor excluyendo títulos que contengan 'Harry' (where published_date between '2023-01-01' and '2023-12-31' and author.name like %Rowling% and title not like %Harry%)
# Limitando conjunto de resultados (list slicing)
books_limited = Book.objects.all()[:5] # Obtener los primeros 5 objetos (equivalente a LIMIT 5)
books_limited = Book.objects.all()[5:10] # Obtener los siguientes 5 objetos (equivalente a LIMIT 5 OFFSET 5)
books_limited = Book.objects.order_by('?')[0] # Obtener el 1 primer libro al azar (equivalente a ORDER BY RAND() LIMIT 1)
# Consulta avanzada _Q para consultas complejas con OR y AND
from django.db.models import Q
# Búsqueda de libros publicados en 2023 o cuyo autor sea 'J.K. Rowling'
books = Book.objects.filter(Q(published_date__year=2023) | Q(author__name__icontains='Rowling')) # Búsqueda con OR (where published_date between '2023-01-01' and '2023-12-31' or author.name like %Rowling%)
books = Book.objects.filter(Q(published_date__year=2023) & ~Q(author__name__icontains='Rowling')) # Búsqueda con AND NOT (where published_date between '2023-01-01' and '2023-12-31' and author.name not like %Rowling%)
for b in books:
    print(b.title, b.published_date, b.author.name)
# Consulta avanzada con F para comparar campos entre sí y evitar hacer consultas adicionales a la base de datos
from django.db.models import F
# Búsqueda de libros cuyo número de páginas sea mayor que el ID del libro
books = Book.objects.filter(pages__gt=F('id')) # Búsqueda con F (where pages > id)
for b in books:
    print(b.title, b.pages, b.id)
# Consulta avanzada con Func para usar funciones de la base de datos
from django.db.models import Func
# Búsqueda de libros cuyo título en mayúsculas contenga 'CATEDRAL'
books = Book.objects.filter(title__icontains=Func('title', function='UPPER')) # Búsqueda con Func (where UPPER(title) like %CATEDRAL%)

# Imaginemos que tenemos un campo de tipo string que guarda una fecha, podemos convertirlo en el tipo fecha con __date
books_in_year = Book.objects.filter(published_string__date=date(2023, 1, 1)) # Búsqueda por año (where published_date = 2023)
for b in books_in_year:
    print(b.title, b.published_date)
print(books_in_year.query) # Ver el SQL generado por el ORM
# Filtrando por valores nulos
books_with_no_date = Book.objects.filter(published_date__isnull=True) # Búsqueda por valores nulos (where published_date is null)
for b in books_with_no_date:
    print(b.title, b.published_date)
print(books_with_no_date.query) # Ver el SQL generado por el ORM
# Obtener objetos o registros por la posición
first = Book.objects.first()
print(first.title, first.author.name)
last = Book.objects.last()
print(last.title, last.author.name)
# Obtener un subconjunto de objetos (paginación)
subset = Book.objects.all()[0:5] # Obtener los primeros 5 objetos (equivalente a LIMIT 5)
for b in subset:
    print(b.title, b.author.name)
# Ordenar objetos por un campo (especificar el campo por el cual se quiere ordenar, por defecto es ascendente)
# Select * from book order by published_date asc;
ordered_books = Book.objects.all().order_by('published_date') # Ordenar por fecha de publicación ascendente
for b in ordered_books:
    print(b.title, b.published_date)
ordered_books_desc = Book.objects.all().order_by('-title') # Ordenar por title descendente
for b in ordered_books_desc:
    print(b.title, b.published_date)
# Ordenar por varios campos
# select * from book inner join author on book.author_id = author.id order by author.name asc, title desc;
ordered_books_multi = Book.objects.all().order_by('author__name', '-title') # Ordenar por autor ascendente y luego por título descendente
for b in ordered_books_multi:
    print(b.title, b.author.name, b.published_date)
print(ordered_books_multi.query) # Obtener el sql generado por el ORM
# Obtener resultados en modo random 
books = Book.objects.order_by('?')[:5] # Obtener 5 libros al azar (mno usar Book.objects.all().order_by('?') pues no funcionaría correctamente)
for b in books:
    print(b.title, b.author.name)
# Filtrar objetos o registros (where)
# Select * from book where author.name = 'J.K. Rowling';
filtered_books = Book.objects.filter(author__name='J.K. Rowling')
for b in filtered_books:
    print(b.title, b.author.name)
filtered_books2 = Book.objects.filter(title__icontains='catedral') # Filtrar por título
for b in filtered_books2:
    print(b.title, b.author.name)
print(filtered_books2.query) # Obtener el sql generado por el ORM
filtered_books3 = Book.objects.filter(title='1984', published_date='1949-06-08') # Filtrar por title y año de publicación
print(filtered_books3.count()) # Contar cuántos libros hay con ese título y año de publicación
print(filtered_books3.exists()) # Verificar si existe algún libro con ese título y año de publicación
print(filtered_books3.first()) # Obtener el primer libro que cumple con el filtro
print(filtered_books3.last()) # Obtener el último libro que cumple con el filtro
print(filtered_books3.values('title', 'author__name')) # Obtener solo los campos title y author.name
print(filtered_books3.values_list('title', 'author__name')) # Obtener solo los campos title y author.name en forma de tupla
print(filtered_books3.query) # Obtener el sql generado por el ORM
# Filtrar con operadores avanzados
# Select * from book where published_date > '2000-01-01';
recent_books = Book.objects.filter(published_date__gt='2000-01-01')
for b in recent_books:
    print(b.title, b.published_date)
# Select * from book where published_date >= '2000-01-01';
recent_books_eq = Book.objects.filter(published_date__gte='2000-01-01')
for b in recent_books_eq:       
    print(b.title, b.published_date)
# Select * from book where published_date < '2000-01-01';
old_books = Book.objects.filter(published_date__lt='2000-01-01')    
for b in old_books:
    print(b.title, b.published_date)

# Actualizar un objeto o registro
book = Book.objects.get(id=1)
book.title = 'Harry Potter and the Sorcerer\'s Stone'       
book.save()
# Actualizar varios objetos a la vez (CUIDADO CON ESTO! puede actualizar muchos registros sin querer)
Book.objects.filter(author__name='J.K. Rowling').update(pages=250) # Actualizar varios registros a la vez (todos los libros de J.K. Rowling tendrán 250 páginas)

# Eliminar un objeto o registro
book = Book.objects.get(id=1)
book.delete()
book = Book.objects.get(title='1984')
book.delete()
# Eliminar varios objetos a la vez (CUIDADO CON ESTO! puede eliminar muchos registros sin querer)
Book.objects.filter(published_date__year__gt=2000).delete() # Eliminar varios registros a la vez (todos los libros publicados antes del año 2000 serán eliminados)
## Comportamientos del on_delete:
## CASCADE: Elimina los registros relacionados (por defecto)
## PROTECT: Evita la eliminación si hay registros relacionados (lanza una excepción)
## SET_NULL: Establece el campo relacionado a NULL (requiere null=True en el campo)
## SET_DEFAULT: Establece el campo relacionado al valor por defecto (requiere default)
## DO_NOTHING: No hace nada (puede causar errores de integridad referencial)
# Soft Delete (eliminación lógica): Sirve para marcar un registro como eliminado sin eliminarlo físicamente de la base de datos
##  En lugar de eliminar el registro, se puede marcar como eliminado con un campo booleano
##  book.is_deleted = True # Marcar el libro como eliminado y ya existe este campo para ello: is_deleted = models.BooleanField(default=False)
##  book.save() # Guardar el cambio
## Book.objects.filter(is_deleted=False) # Filtrar solo los libros que no están eliminados

# Aggregates
# A diferencia de annotate, aggregate devuelve un diccionario con los resultados de la agregación y no un QuerySet de objetos, por lo que no se pueden encadenar más filtros o métodos después de un aggregate y siempre devuelve un solo resultado global y no varios como con annotate.
from django.db.models import Count, Avg, Max, Min, Sum
# Contar cuántos libros hay en la base de datos
book_count = Book.objects.aggregate(total_libros = Count('id'))
print(f'Total de libros: {book_count['total_libros']}')
# Contar cuántos autores hay en la base de datos
author_count = Author.objects.aggregate(total_autores = Count('id'))['total_autores']
print(f'Total de autores: {author_count}')
# Calcular el promedio de páginas de todos los libros
average_pages = Book.objects.aggregate(promedio_paginas = Avg('pages'))['promedio_paginas']
print(f'Promedio de páginas: {average_pages}')
# Calcular el número máximo de páginas de un libro
max_pages = Book.objects.aggregate(maximo_paginas = Max('pages'))['maximo_paginas']
# SELECT MAX("minilibrary_book"."pages") AS "maximo_paginas" FROM "minilibrary_book"
print(f'Máximo de páginas: {max_pages}') 
# Conocer el sql generado por el ORM
from django.db import connection
print(connection.queries) # Ver todas las consultas SQL ejecutadas en la base de datos hasta el momento

# Annotate
# A diferencia de aggregate, annotate devuelve un QuerySet de objetos con los resultados de la agregación y se pueden encadenar más filtros o métodos después de un annotate y devuelve varios resultados, uno por cada objeto en el QuerySet.
from django.db.models import Count, Avg
# Contar cuántos libros tiene cada autor
authors_with_book_count = Author.objects.annotate(book_count=Count('books')) # Aquí 'books' es el related_name definido en el modelo Book para el campo ForeignKey author y de esta forma se cuenta cuántos libros tiene cada autor 
for author in authors_with_book_count:
    print(f'Autor: {author.name}, Número de libros: {author.book_count}')
# Calcular el promedio de páginas por autor
authors_with_avg_pages = Author.objects.annotate(avg_pages=Avg('books__pages')) # Aquí 'books' es el related_name definido en el modelo Book para el campo ForeignKey author
for author in authors_with_avg_pages:
    print(f'Autor: {author.name}, Promedio de páginas: {author.avg_pages}')
# SQL generado por el ORM
print(authors_with_avg_pages.query) # Ver el SQL generado por el ORM
# SELECT "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date", AVG("minilibrary_book"."pages") AS "avg_pages" FROM "minilibrary_author" LEFT OUTER JOIN "minilibrary_book" ON ("minilibrary_author"."id" = "minilibrary_book"."author_id") GROUP BY "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date"

# Transaction atomic (Transacciones atómicas)
from django.db import transaction, IntegrityError
# Realizar varias operaciones de base de datos de forma atómica (si una falla, se revierten todas)
try:
    with transaction.atomic():
        author = Author.objects.create(name='New Author', birth_date='1970-01-01')
        book1 = Book.objects.create(title='New Book 1', published_date='2023-01-01', author=author, pages=100, isbn='9780000000001')
        book2 = Book.objects.create(title='New Book 2', published_date='2023-01-01', author=author, pages=150, isbn='9780000000002')
        # Simular un error para probar la transacción atómica
        raise Exception('Simulated error')
except IntegrityError as e:
    print(f'Transaction rolled back due to integrity error: {e}')
except Exception as e:
    print(f'Transaction rolled back due to error: {e}')
# Verificar que no se crearon los registros debido al error
print(Author.objects.filter(name='New Author').exists()) # Debería ser False
print(Book.objects.filter(title='New Book 1').exists()) # Debería ser False
print(Book.objects.filter(title='New Book 2').exists()) # Debería ser False

# Sección 9: Relaciones entre modelos y optimización de consultas

# Relación entre modelos (ForeignKey, OneToOneField, ManyToManyField)
# ForeignKey: Relación uno a muchos (un autor puede tener muchos libros)
# OneToOneField: Relación uno a uno (un perfil de usuario tiene un solo usuario)
# ManyToManyField: Relación muchos a muchos (un libro puede tener muchos géneros y un género puede tener muchos libros)
# unique y primary_key son mutuamente excluyentes en los campos de un modelo, es decir, no se pueden usar ambos al mismo tiempo en un mismo campo.
#   class Book(models.Model):
#       title = models.CharField(max_length=200, unique=True) # El título del libro debe ser único
#       author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') # Un autor puede tener muchos libros, related_name permite acceder a los libros de un autor con author.books.all()
#   class Author(models.Model):
#       name = models.CharField(max_length=100)
#       birth_date = models.DateField()
#       profile = models.OneToOneField(User, on_delete=models.CASCADE) # Un perfil de usuario tiene un solo usuario
#   class Genre(models.Model):
#       name = models.CharField(max_length=100, unique=True)
#       books = models.ManyToManyField(Book, related_name='genres') # Un libro puede tener muchos géneros y un género puede tener muchos libros 
# Crear un autor y varios libros relacionados
author = Author.objects.create(name='Gabriel García Márquez', birth_date='1927-03-06')
book1 = Book.objects.create(title='Cien años de soledad', published_date='1967-05-30', author=author, pages=417, isbn='1780307474728')
book2 = Book.objects.create(title='El amor en los tiempos del cólera', published_date='1985-03-05', author=author, pages=348, isbn='1780307389732')
# Acceder al autor desde un libro (relación directa)
print(f'Libro: {book1.title}, Autor: {book1.author.name} Birth Date: {book1.author.birth_date}') # Acceder al autor desde un libro (relación directa) usando el campo ForeignKey author
print(author.id, author.name, author.birth_date, author.books.all()) # Acceder a los libros de un autor (relación inversa) usando el related_name 'books' definido en el modelo Book para el campo ForeignKey author (relación inversa o related_name)
# Consultar libros de un autor (relación inversa)
books_by_author = author.books.all() # Aquí 'books' es el related_name definido en el modelo Book para el campo ForeignKey author
for book in books_by_author:
    print(f'Libro: {book.title}, Autor: {book.author.name}')
finction = Genre.objects.create(name='Ficción')
fantasy = Genre.objects.create(name='Fantasía')
drama = Genre.objects.create(name='Drama')
# Sí existiera un género ya creado se podría usar get_or_create para no crear duplicados:
# finction, created = Genre.objects.get_or_create(name='Ficción') # Si el género ya existe, no se crea uno nuevo, created será False sí no se creó

orwell = Author.objects.get(name='George Orwell')
book3 = Book.objects.create(title='1984', published_date='1949-06-08', author=orwell, pages=328, isbn='9780451533335')
book3.genres.add(finction, drama) # Añadir géneros a un libro (relación muchos a muchos)
rowling = Author.objects.get(name='J.K. Rowling')
book4 = Book.objects.create(title='Harry Potter and the Chamber of Secrets', published_date='1998-07-02', author=rowling, pages=251, isbn='97807472228493')
book4.genres.add(fantasy, drama) # Añadir géneros a un libro (relación muchos a muchos)
# Consultar géneros de un libro (relación directa)
book = Book.objects.get(title='1984')
for genre in book.genres.all(): # Aquí 'genres' es el related_name definido en el modelo Book para el campo ManyToManyField genres
    print(f'Género: {genre.name}')
# Consultar libros de un género (relación inversa)
genre = Genre.objects.get(name='Drama')
for book in genre.books.all(): # Aquí 'books' es el related_name definido en el modelo Genre para el campo ManyToManyField books
    print(f'Libro: {book.title}, Género: {genre.name}')
for book in fiction.books.all(): # Aquí 'books' es el related_name definido en el modelo Genre para el campo ManyToManyField books, en este caso se accede a los libros del género Ficción y se imprime el título del libro y el nombre del género
    print(f'Libro: {book.title}, Género: {fiction.name}')

book = Book.objects.get(title='1984')
detail = BookDetail.objects.create(book=book, summary='A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism.', language='English', publisher='Secker & Warburg', cover_url='https://example.com/1984.jpg')
print(f'Book: {detail.book.title}, Summary: {detail.summary}, Language: {detail.language}, Publisher: {detail.publisher}, Cover URL: {detail.cover_url}') # Acceder al libro desde el detalle del libro (relación directa)
book_detail = BookDetail.objects.get(book__title='1984') # Aquí 'book' es el nombre del campo OneToOneField en el modelo BookDetail
print(f'Book: {book_detail.book.title}, Summary: {book_detail.summary}, Language: {book_detail.language}, Publisher: {book_detail.publisher}, Cover URL: {book_detail.cover_url}') # Acceder al libro desde el detalle del libro (relación directa)

# Optimización de consultas con select_related (solo para foreignkeys y OneToOne keys) y prefetch_related
# Problema N+1: Ocurre cuando se hacen muchas consultas a la base de datos innecesarias al acceder a relaciones entre modelos, por ejemplo, al iterar sobre un conjunto de objetos y acceder a un campo relacionado en cada iteración. Entonces por cada objeto que se recorre, se hace una consulta adicional a la base de datos para obtener el objeto relacionado, lo que puede generar muchas consultas y afectar el rendimiento.
# Solución: Usar select_related y prefetch_related para reducir el número de consultas a la base de datos.
# select_related se usa para relaciones ForeignKey y OneToOne, hace un JOIN y trae los datos relacionados en una sola consulta/llamada sin hacer consultas adicionales a la base de datos
# prefetch_related se usa para relaciones ManyToMany y reverse ForeignKey, hace una consulta adicional y luego une los datos en Python
# Obtener todos los libros con sus autores usando select_related (evita consultas adicionales a la base de datos)
# Sin optimizar con select_related:
books = Book.objects.all() # Aquí se hace 1 consulta a la base de datos
for book in books:
    print(f'Libro: {book.title}, Autor: {book.author.name}') # Aquí se hace 1 consulta adicional por cada libro para obtener el autor (N consultas adicionales)
# SQL generado por el ORM 
print(books.query) # Ver el SQL generado por el ORM
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn" FROM "minilibrary_book"
# Y por cada libro se haría otra consulta para obtener el autor:
    # SELECT "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date" FROM "minilibrary_author" WHERE "minilibrary_author"."id" = %s  [1]
    # SELECT "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date" FROM "minilibrary_author" WHERE "minilibrary_author"."id" = %s  [2]
    # SELECT "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date" FROM "minilibrary_author" WHERE "minilibrary_author"."id" = %s  [3]
    # ...

# Con select_related se hace 1 sola consulta a la base de datos con un JOIN y se traen los datos relacionados de los autores de una sola vez:
books_with_authors = Book.objects.select_related('author').all() # Aquí 'author' es el nombre del campo ForeignKey en el modelo Book
for book in books_with_authors:
    print(f'Libro: {book.title}, Autor: {book.author.name}')
# SQL generado por el ORM
print(books_with_authors.query) # Ver el SQL generado por el ORM
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn", "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date" FROM "minilibrary_book" INNER JOIN "minilibrary_author" ON ("minilibrary_book"."author_id" = "minilibrary_author"."id") 


# Obtener todos los autores con sus libros usando prefetch_related (evita consultas adicionales a la base de datos) y funciona en relaciones inversas y ManyToMany
# Sin optimizar con prefetch_related:
genres = Genre.objects.all() # Aquí se hace 1 consulta a la base de datos
for genre in genres:
    for book in genre.books.all(): # Aquí se hace 1 consulta adicional por cada género para obtener sus libros (N consultas adicionales)
        print(f'Género: {genre.name}, Libro: {book.title}')
# Con prefetch_related se hace 2 consultas a la base de datos, una para los géneros y otra para los libros, y luego une los datos en Python:
genres_with_books = Genre.objects.prefetch_related('books').all() # Aquí 'books' es el related_name definido en el modelo Genre para el campo ManyToManyField books
for genre in genres_with_books:
    print(f'Género: {genre.name}')
    for book in genre.books.all():
        print(f' - Libro: {book.title}')
# SQL generado por el ORM
print(genres_with_books.query) # Ver el SQL generado por el ORM
# SELECT "minilibrary_genre"."id", "minilibrary_genre"."name" FROM "minilibrary_genre"
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn", "minilibrary_genre_books"."genre_id" FROM "minilibrary_book" INNER JOIN "minilibrary_genre_books" ON ("minilibrary_book"."id" = "minilibrary_genre_books"."book_id") WHERE "minilibrary_genre_books"."genre_id" IN (%s, %s)  [1, 2]
# Y con prefetch_related se haría una consulta para obtener todos los registros relacionados de los libros de una sola vez:
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn", "minilibrary_genre_books"."genre_id" FROM "minilibrary_book" INNER JOIN "minilibrary_genre_books" ON ("minilibrary_book"."id" = "minilibrary_genre_books"."book_id") WHERE "minilibrary_genre_books"."genre_id" IN (%s, %s, %s)  [1, 2, 3]
# Obtener todos los autores con sus libros usando prefetch_related (evita consultas adicionales a la base de datos) y funciona en relaciones inversas y ManyToMany
authors = Author.objects.all() # Aquí se hace 1 consulta a la base de datos
for author in authors:
    for book in author.books.all(): # Aquí se hace 1 consulta adicional por cada autor para obtener sus libros (N consultas adicionales)
        print(f'Autor: {author.name}, Libro: {book.title}')
# Con prefetch_related se hace 2 consultas a la base de datos, una para los autores y otra para los libros, y luego une los datos en Python:
authors_with_books = Author.objects.prefetch_related('books').all() # Aquí 'books' es el related_name definido en el modelo Book para el campo ForeignKey author
for author in authors_with_books:
    print(f'Autor: {author.name}')
    for book in author.books.all():
        print(f' - Libro: {book.title}')    
# SQL generado por el ORM
print(authors_with_books.query) # Ver el SQL generado por el ORM
# SELECT "minilibrary_author"."id", "minilibrary_author"."name", "minilibrary_author"."birth_date" FROM "minilibrary_author"
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn" FROM "minilibrary_book" WHERE "minilibrary_book"."author_id" IN (%s, %s, %s)  [1, 2, 3]    
# Con prefetch_related se haría una sola consulta para obtener todos los registros relacionados de los libros de una sola vez:
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn" FROM "minilibrary_book" inner join "minilibrary_author" ON ("minilibrary_book"."author_id" = "minilibrary_author"."id") WHERE "minilibrary_book"."author_id"  

# Consultas con relaciones (JOINs)
##  Obtener todos los libros de un autor específico
books_by_rowling = Book.objects.filter(author__name='J.K. Rowling') # Filtrar libros por el nombre del autor (JOIN implícito), aquí author es el nombre del campo ForeignKey en el modelo Book
# Ver el resultado SQL generado por el ORM
print(Book.objects.filter(author__name='J.K. Rowling').query) # Ver el SQL generado por el ORM
## En el caso de un insert o get_or_create no se puede ver el SQL generado directamente, pero se puede usar el logging de Django para ver las consultas SQL ejecutadas en la base de datos.
from django.db import connection
# Author.objects.get_or_create(
#     name="Mario Vargas Llosa",
#     defaults={"birth_date": "1936-03-28"}
# )
for q in connection.queries:
    print(q["sql"]) # Ver todas las consultas SQL ejecutadas en la base de datos hasta el momento
## También se puede ejecutar este código al inicio del shell de Django para ver todas las consultas SQL generadas por el ORM en la consola:
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# Otra forma de ver las consultas SQL generadas por el ORM es configurando el logging en settings.py:
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,      
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
# Ahora al ejecutar cualquier consulta se verá el SQL generado en la consola
book, created = Book.objects.get_or_create(title='New Book', defaults={'published_date': '2023-01-01', 'author': rowling, 'pages': 100,

# Modelo User
## Es un modelo que viene por defecto en Django para manejar usuarios y autenticación
## python3 manage.py shell
from django.contrib.auth.models import User
# Crear un nuevo usuario
new_user = User.objects.create_user(username='newuser', password='password123')
print(new_user.username, new_user.is_staff, new_user.is_superuser) # Acceder a los campos del modelo User
# Crear un superusuario
super_user = User.objects.create_superuser(username='admin', password='admin123')
print(super_user.username, super_user.is_staff, super_user.is_superuser) # Acceder a los campos del modelo User
# Autenticar un usuario
from django.contrib.auth import authenticate
user = authenticate(username='newuser', password='password123')
if user is not None:
    print(f'Usuario autenticado: {user.username}')
else:
    print('Credenciales inválidas')
# Cambiar la contraseña de un usuario
user = User.objects.get(username='newuser')
user.set_password('newpassword123')
user.save()
# Verificar la nueva contraseña
user = authenticate(username='newuser', password='newpassword123')
if user is not None:
    print(f'Usuario autenticado con nueva contraseña: {user.username}')
else:
    print('Credenciales inválidas con nueva contraseña')
# Listar todos los usuarios
users = User.objects.all()
for u in users:
    print(u.username, u.is_staff, u.is_superuser)


## Crear un perfil de usuario extendiendo el modelo User con OneToOneField
# myapp/models.py
from django.contrib.auth.models import User
from django.db import models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relación uno a uno con el modelo User
    bio = models.TextField(blank=True, null=True) # Campo adicional para la biografía del usuario
    birth_date = models.DateField(blank=True, null=True) # Campo adicional para la fecha de nacimiento del usuario
    def __str__(self):
        return self.user.username
# Crear un perfil de usuario para un usuario existente
user = User.objects.get(username='newuser')
profile = UserProfile.objects.create(user=user, bio='This is my bio.', birth_date='1990-01-01')
print(profile.user.username, profile.bio, profile.birth_date) # Acceder a los campos del modelo UserProfile
# Acceder al perfil de usuario desde el modelo User (relación inversa)
user = User.objects.get(username='newuser')
print(user.userprofile.bio, user.userprofile.birth_date) # Aquí 'userprofile' es el nombre del modelo UserProfile en minúsculas
# Realizar migraciones para crear la tabla del modelo UserProfile en la base de datos
# python manage.py makemigrations
# python manage.py migrate

## Otra forma de acceder al modelo User más fácilmente (recomendado) y evitar problemas si se usa un modelo User personalizado en settings.py
from django.contrib.auth import get_user_model
User = get_user_model() # Obtener el modelo User actual (puede ser el modelo por defecto o un modelo personalizado)
user = User.objects.get(username='newuser') # Usar el modelo User para hacer consultas
print(user.username, user.is_staff, user.is_superuser) # Acceder a los campos del modelo User
## Crear un usuario con el modelo User obtenido con get_user_model
new_user2 = User.objects.create_user(username='anotheruser', email='anotheruser@example.com', password='password123', first_name='Another', last_name='User')
print(new_user2.username, new_user2.is_staff, new_user2.is_superuser) # Acceder a los campos del modelo User
user= User.objects.get(username='anotheruser')
print(user.username, user.email, user.first_name, user.last_name) # Acceder a los campos del modelo User

book = Book.objects.create(title='Django for Beginners', published_date='2023-01-01', author=rowling, pages=300, isbn='9780000000003')
print(book.title, book.author.name) # Acceder a los campos del modelo Book
review = Review.objects.create(book=book, user=user, rating=5, text='Great book for learning Django!')
print(f'Review for {review.book.title} by {review.user.username}: {review.rating}/5 - {review.text}')

Loan.objects.create(book=book, user=user, loan_date='2023-10-01', return_date='2023-10-15')
loans = Loan.objects.all()
for loan in loans:
    print(f'Loan: {loan.book.title} to {loan.user.username} from {loan.loaned_date} to {loan.returned_date} ({'Returned' if loan.is_returned else 'Not Returned'})')
returned_loans = Loan.objects.filter(is_returned=False)
for loan in returned_loans:
    print(f'Returned Loan: {loan.book.title} to {loan.user.username} from {loan.loaned_date} to {loan.returned_date} ({'Returned' if loan.is_returned else 'Not Returned'})')   

from django.utils import timezone
loan = Loan.objects.get(id=1)
loan.returned_date = timezone.now()
loan.is_returned = True
loan.save()
print(f'Loan updated: {loan.book.title} to {loan.user.username} from {loan.loaned_date} to {loan.returned_date} ({'Returned' if loan.is_returned else 'Not Returned'})')

## Definir un modelo personalizado que extienda el modelo User de Django. Agregar al final de settings.py:
# AUTH_USER_MODEL = 'myapp.CustomUser' # Aquí 'myapp' es el nombre de la aplicación donde se define el modelo CustomUser
# Crear un modelo personalizado que extienda el modelo User de Django y agregar campos adicionales como bio y birth_date
# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True) # Campo adicional para la biografía del usuario
    birth_date = models.DateField(blank=True, null=True) # Campo adicional para la fecha de nacimiento del usuario
    def __str__(self):
        return self.username
# Realizar migraciones para crear la tabla del modelo CustomUser en la base de datos
# python manage.py makemigrations
# python manage.py migrate
# Crear un nuevo usuario con el modelo personalizado
custom_user = CustomUser.objects.create_user(username='customuser', password='password123', bio='This is a custom user.', birth_date='1990-01-01')
print(custom_user.username, custom_user.bio, custom_user.birth_date) # Acceder a los campos del modelo CustomUser


# Uso de through en ManyToManyField para agregar campos adicionales a la relación en una tabla intermedia
# myapp/models.py 
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first() # Obtener el primer usuario
book = Book.objects.first() # Obtener el primer libro
Recomendation.objects.create(user=user, book=book, note='Great book for learning Django!') # Crear una recomendación con campos adicionales en la tabla intermedia
# Sí no lo hicieramos así, no podríamos agregar la nota a la recomendación, que es un campo intermedio en la relación ManyToMany entre User y Book que hemos creado con el modelo Recomendation y el parámetro through en el campo ManyToManyField  

# Seeds o datos iniciales
# Importar datos iniciales desde un archivo python seeds/seeds.py
# python3 manage.py shell < seeds/seeds.py
# Importar datos iniciales desde un archivo JSON
# python3 manage.py loaddata seeds/initial_data.json
# Exportar datos a un archivo JSON
# python3 manage.py dumpdata minilibrary > seeds/initial_data.json


# Consultas avanzadas 
from django.db.models import Count, Avg 
# Contar sí alguno de los libros tiene alguna reseña y un promedio de calificaciones > 1.5
books_with_reviews = Book.objects.annotate(num_reviews=Count('reviews'), avg_rating=Avg('reviews__rating')).filter(num_reviews__gt=1, avg_rating__gt=1.5)
for book in books_with_reviews:
    print(f'Book: {book.title}, Review Count: {book.num_reviews}, Average Rating: {book.avg_rating}')
# SQL generado por el ORM
print(books_with_reviews.query) # Ver el SQL generado por el ORM
# SELECT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn", COUNT("minilibrary_review"."id") AS "num_reviews", AVG("minilibrary_review"."rating") AS "avg_rating" FROM "minilibrary_book" LEFT OUTER JOIN "minilibrary_review" ON ("minilibrary_book"."id" = "minilibrary_review"."book_id") GROUP BY "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."published_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn" HAVING COUNT("minilibrary_review"."id") > 0 AND AVG("minilibrary_review"."rating") > 1.5

# Buscar libros actualmente prestados (no devueltos)
Book.objects.filter(loans__is_returned=False).distinct() # Aquí 'loans' es el related_name definido en el modelo Loan para el campo ForeignKey book, distinct() se usa para evitar duplicados sí un libro tiene varios préstamos no devueltos
# SQL generado por el ORM
print(Book.objects.filter(loans__is_returned=False).distinct().query) # Ver el SQL generado por el ORM
# SELECT DISTINCT "minilibrary_book"."id", "minilibrary_book"."title", "minilibrary_book"."publication_date", "minilibrary_book"."author_id", "minilibrary_book"."pages", "minilibrary_book"."isbn" FROM "minilibrary_book" INNER JOIN "minilibrary_loan" ON ("minilibrary_book"."id" = "minilibrary_loan"."book_id") WHERE NOT "minilibrary_loan"."is_returned"

# Libros sin reviews
Book.objects.filter(reviews__isnull=True) # Aquí 'reviews' es el related_name definido en el modelo Review para el campo ForeignKey book
Book.objects.annotate(num_reviews=Count('reviews')).filter(num_reviews=0) # Otra forma de obtener libros sin reviews

from django.contrib.auth import get_user_model
User = get_user_model()
# Usuarios con más de 2 préstamos
users_with_many_loans = User.objects.annotate(loan_count=Count('loans')).filter(loan_count__gt=2) # Aquí 'loans' es el related_name definido en el modelo Loan para el campo ForeignKey user
for user in users_with_many_loans:
    print(f'User: {user.username}, Loan Count: {user.loan_count}')
# SQL generado por el ORM
print(users_with_many_loans.query) # Ver el SQL generado por el ORM
```

References: 

- Django ORM documentation: https://docs.djangoproject.com/en/5.2/topics/db/models/
- Django Fields documentation: https://docs.djangoproject.com/en/5.2/ref/models/fields/
- Django QuerySet API reference: https://docs.djangoproject.com/en/5.2/ref/models/querysets/
- Django Migrations documentation: https://docs.djangoproject.com/en/5.2/topics/migrations/
- Django Admin documentation: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/
- Django Database API reference: https://docs.djangoproject.com/en/5.2/ref/databases/
- Django Relationships documentation: https://docs.djangoproject.com/en/5.2/topics/db/models/#relationships
- Django Aggregation documentation: https://docs.djangoproject.com/en/5.2/topics/db/aggregation/
- Django Query Expressions documentation: https://docs.djangoproject.com/en/5.2/ref/models/expressions/
- Django Transactions documentation: https://docs.djangoproject.com/en/5.2/topics/db/transactions/
- Django Custom Managers documentation: https://docs.djangoproject.com/en/5.2/topics/db/managers/
- Django Raw SQL documentation: https://docs.djangoproject.com/en/5.2/topics/db/sql/
- Django Performance optimization documentation: https://docs.djangoproject.com/en/5.2/topics/performance/
- Django Testing with ORM documentation: https://docs.djangoproject.com/en/5.2/topics/testing/tools/#testing-with-the-orm


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

