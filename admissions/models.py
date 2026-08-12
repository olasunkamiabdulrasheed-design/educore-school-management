from django.db import models
from academics.models import Class
from django.urls import reverse

class AdmissionApplication(models.Model):

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    # Student Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Academic Information
    applying_for = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        related_name="admission_applications"
    )

    previous_school = models.CharField(
        max_length=255,
        blank=True
    )

    # Parent / Guardian Information
    guardian_name = models.CharField(max_length=150)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField(blank=True)
    guardian_relationship = models.CharField(
        max_length=100,
        blank=True
    )

    # Application Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # System timestamps
    application_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-application_date"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applying_for}"

    def get_success_url(self):
        return reverse(
            "admissions:detail",
            kwargs={"pk": self.object.pk}
    )


