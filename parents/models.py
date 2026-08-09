from django.db import models
from accounts.models import User
from students.models import Student


class Parent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="parent_profile"
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    children = models.ManyToManyField(
        Student, related_name="parents", blank=True
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"