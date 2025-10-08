from .module import Module
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from ..fields import OrderField


class ItemBase(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_related', on_delete=models.CASCADE)
    # '%(class)s_related' se reemplaza por el nombre del modelo en minúsculas y añade '_related' lo que crea una relación inversa única para cada subclase y de forma dinámica, 
    # ejemplo: text_related, file_related, image_related, video_related
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # Esto indica que es una clase abstracta y no se creará una tabla en la base de datos para este modelo.

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
    
# En este caso anterior, cada subclase (Text, File, Image, Video) hereda de ItemBase, lo que significa que cada una tendrá los campos owner, title, created_at y updated_at, además de sus propios campos específicos: content para Text, file para File e Image, y url para Video,
# de esta forma se evita la duplicación de código y se mantiene una estructura clara y organizada.


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        'model__in': ('text', 'video', 'image', 'file')
    })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']