from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    recommended_by = models.ManyToManyField(get_user_model(), through='Recommendation', related_name='recommendations')
    # through='Recommendation' specifies the intermediary model for the many-to-many relationship defined below for us
    # related_name='recommendations' allows us to access the books a user has recommended via user.recommendations
    # Aquí perdemos la capacidad de usar recommended_by para acceder a los usuarios que recomendaron un libro, pero ganamos la capacidad de agregar campos adicionales a la relación a través del modelo Recommendation.
    # también perdemos el acceso al método add() y remove() para manejar la relación many-to-many directamente, pero podemos manejar la relación a través del modelo Recommendation.

    class Meta:
        verbose_name = 'libro'
        verbose_name_plural = 'libros'

    def __str__(self):
        return self.title

class BookDetail(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='detail')
    summary = models.TextField(null=True, blank=True)
    # cover_url = models.URLField(null=True, blank=True)
    cover_url = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=30, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Details of {self.book.title}" 
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews') # Using get_user_model for flexibility
    rating = models.PositiveBigIntegerField()
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username} ({self.rating}/5)"

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan of {self.book.title} to {self.user.username} ({'Returned' if self.is_returned else 'Not Returned'})"
    
class Recommendation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recommended_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    class Meta:
        unique_together = ('user', 'book')  # Ensure a user can't recommend the same book multiple times

    def __str__(self):
        return f"{self.book.title} recommended by {self.user.username}"