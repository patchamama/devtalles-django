from django.db import models

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
    published_date = models.DateField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)

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
