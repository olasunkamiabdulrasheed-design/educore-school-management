from django.db import models
from teachers.models import Teacher


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=30, unique=True)
    level = models.CharField(max_length=30, blank=True)
    class_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="classes_taught"
    )
    subjects = models.ManyToManyField(Subject, blank=True, related_name="classes")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name