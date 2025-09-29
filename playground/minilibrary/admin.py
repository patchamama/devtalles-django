from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

admin.site.site_header = "Mi Biblioteca Admin"  # Cambia el header del admin
admin.site.site_title = "Mi Biblioteca"  # Cambia el título del admin
admin.site.index_title = "Panel de Administración"  # Cambia el título de la página principal del admin

User = get_user_model()

class LoanInline(admin.TabularInline):
    model = Loan
    extra = 1  # Número de formularios adicionales para agregar nuevos préstamos
    # fields = ('user', 'loan_date', 'return_date', 'is_returned') # Campos a mostrar en el inline
    # readonly_fields = ('loan_date',)  # Hacer que el campo loan_date sea de solo lectura
    # show_change_link = True  # Muestra un enlace para editar el préstamo completo
    
class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]  # Muestra los préstamos inline en la página de detalle del usuario
    list_display = ('username', 'email') # Campos a mostrar en la lista de usuarios
    # search_fields = ('username', 'email', 'first_name', 'last_name') # Campos por los que se puede buscar
    # list_filter = ('is_staff', 'is_superuser', 'is_active') # Filtros para la barra lateral
    # ordering = ('username',) # Ordenar por nombre de usuario    
    
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Número de formularios adicionales para agregar nuevas reseñas
    # fields = ('user', 'rating', 'comment') # Campos a mostrar en el inline
    # readonly_fields = ('created_at',)  # Hacer que el campo created_at sea de solo lectura
    # show_change_link = True  # Muestra un enlace para editar la reseña completa

class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False # Evita que se pueda eliminar el detalle del libro desde el inline
    verbose_name_plural = 'Detalles del libro' # Nombre plural en la interfaz
    # fk_name = 'book' # Especifica el campo ForeignKey si hay múltiples relaciones al mismo modelo
    
    
@admin.register(Genre)  # decorador que hace lo mismo que admin.site.register(Genre, GenreAdmin)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',) # Campos por los que se puede buscar
    ordering = ('name',) # Ordenar por nombre

@admin.register(Author)  # decorador que hace lo mismo que admin.site.register(Author, AuthorAdmin)
class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('name', 'birth_date') # Campos a mostrar en la lista de autores
    search_fields = ('name',) # Campos por los que se puede buscar
    # ordering = ('name',) # Ordenar por nombre
    # inlines = [LoanInline]  # Muestra los préstamos inline en la página de detalle del autor (a través de los libros del autor)

@admin.register(Book)  # decorador que hace lo mismo que admin.site.register(Book, BookAdmin)
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]  # Muestra las reseñas y detalles del libro inline en la página de detalle del libro
    list_display = ('title', 'author', 'pages', 'publication_date') # Campos a mostrar en la lista de libros
    search_fields = ('title', 'author__name') # Campos por los que se puede buscar
    list_filter = ('genres', 'publication_date', 'author') # Filtros para la barra lateral
    ordering = ('-publication_date',) # Ordenar por fecha de publicación descendente
    date_hierarchy = 'publication_date'  # Agrega una jerarquía de fechas para facilitar la navegación por años/meses/días
    autocomplete_fields = ['author', 'genres'] # Habilita la búsqueda por autocompletado para los campos ForeignKey y ManyToMany en este caso author debe de tener un índice en la base de datos para que funcione bien y en el admin del modelo Author debe estar definido search_fields = ('name',) para que funcione bien
    # fields = ('title', 'author', 'publication_date', 'pages', 'isbn', 'genres') # Campos a mostrar en el formulario de edición
    
    fieldsets = (
        ("Información general", {
            'fields': ('title', 'author', 'publication_date', 'genres')
        }),
        ('Detalles', {
            'classes': ('collapse',),  # Hace que este campo sea colapsable
            'fields': ('isbn', 'pages'),
        }),
    )
    
    def has_add_permission(self, request):
        return request.user.is_superuser # Solo los superusuarios pueden agregar libros, es decir sí request.user.is_superuser=True entonces se permite agregar libros
        # Si queremos limitar el número de libros que se pueden agregar, podemos hacer algo como esto:
        # # Permitir agregar solo si hay menos de 100 libros
        # if self.model.objects.count() >= 100:
        #     return False
        # return super().has_add_permission(request)
        
    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
        # Solo los superusuarios y el personal (staff) pueden editar libros, es decir sí request.user.is_superuser=True o request.user.is_staff=True entonces se permite editar libros
        # return super().has_change_permission(request, obj) # Permitir a todos los usuarios con permiso de cambio editar libros 
    
@admin.action(description='Marcar préstamos como devueltos')
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True)

@admin.register(Loan)  # decorador que hace lo mismo que admin.site.register(Loan, LoanAdmin)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'loan_date', 'is_returned') # Campos a mostrar en la lista de préstamos
    readonly_fields = ('loan_date',)  # Hacer que el campo loan_date sea de solo lectura, se pone al final una coma porque es una tupla
    actions = [mark_as_returned] # Registrar la acción en el admin
    raw_id_fields = ['user', 'book']  # Usa un campo de entrada de ID en lugar de un menú desplegable para el campo book, útil si hay muchos libros

# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
# admin.site.register(Loan, LoanAdmin)
admin.site.register(Recommendation)

try:
    # Desregistrar el modelo User predeterminado si está registrado (para evitar errores) y luego registrar el personalizado
    # Por qué? Porque si no, al hacer admin.site.register(User, CustomUserAdmin) nos da error porque ya está registrado
    # Y por defecto, Django registra el modelo User con el UserAdmin predeterminado al iniciar la app admin y por eso se muestra en el admin
    admin.site.unregister(User) 
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin) # Registrar el modelo User otra vez con la configuración personalizada del administrador 
