from django.db import models
from django.conf import settings
from .course import Course

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # Assuming rating is an integer value
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # A user can only review a course once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - Rating: {self.rating}"