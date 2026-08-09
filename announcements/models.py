from django.db import models
from accounts.models import User


class Announcement(models.Model):
    class Audience(models.TextChoices):
        EVERYONE = "EVERYONE", "Everyone"
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teachers"
        STUDENT = "STUDENT", "Students"
        PARENT = "PARENT", "Parents"

    title = models.CharField(max_length=150)
    body = models.TextField()
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.EVERYONE)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="announcements")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title