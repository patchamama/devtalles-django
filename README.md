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



