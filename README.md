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

