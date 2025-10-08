from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_instructor_profile(sender, instance, created, **kwargs):
    if created and instance.is_instructor:
        InstructorProfile.objects.create(user=instance)
        
# se crear un decorador que escucha la señal post_save del modelo de usuario personalizado definido en settings.AUTH_USER_MODEL.
# Cuando se crea un nuevo usuario y si el campo is_instructor es True, se crea automáticamente un perfil de instructor asociado a ese usuario.  
# Esto asegura que cada vez que se registre un nuevo instructor, su perfil de instructor se cree automáticamente sin necesidad de intervención manual.