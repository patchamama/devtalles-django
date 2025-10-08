from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    # Por default, AbstractUser already includes:
    # username, first_name, last_name, email, password, is_staff, is_active, date_joined, etc.
    
    def __str__(self):
        return self.get_full_name() or self.username # Return full name if available (no es obligatorio), else username