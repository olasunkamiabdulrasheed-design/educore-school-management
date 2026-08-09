from django.db import models
from accounts.models import User


class Teacher(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    gender = models.CharField(
    max_length=10,
    choices=[
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]
    )

    date_of_birth = models.DateField()

    subject_specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    date_joined = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last = Teacher.objects.order_by("-id").first()
            next_number = (last.id + 1) if last else 1
            self.employee_id = f"EMP{next_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name() or self.user.username