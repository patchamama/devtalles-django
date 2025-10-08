from django.db import models
from django.conf import settings

class InstructorProfile(models.Model):
    # One-to-one relationship with the custom User model defined in settings.AUTH_USER_MODEL 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    social_network = models.URLField(blank=True)

    def __str__(self):
        return f"Instructor Profile: {self.user.get_full_name() or self.user.username}"