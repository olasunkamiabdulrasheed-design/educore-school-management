from django.db import models
from students.models import Student
from academics.models import Class


class AdmissionApplication(models.Model):

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    reference = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Student Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    applying_for = models.ForeignKey(Class, on_delete=models.PROTECT, related_name="admission_applications")
    previous_school = models.CharField(max_length=255, blank=True)

    guardian_name = models.CharField(max_length=150)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField(blank=True)
    guardian_relationship = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Set once approved — links this application to the resulting enrolled Student
    student = models.OneToOneField(
        Student, on_delete=models.SET_NULL, null=True, blank=True, related_name="admission_application"
    )

    application_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-application_date"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applying_for}"



    def save(self, *args, **kwargs):
        if not self.reference:
            from django.utils import timezone

            year = timezone.now().year

            last_application = (
                AdmissionApplication.objects
                .filter(reference__startswith=f"ADM-{year}-")
                .order_by("-reference")
                .first()
            )

            if last_application and last_application.reference:
                try:
                    last_number = int(last_application.reference.split("-")[-1])
                except (ValueError, IndexError):
                    last_number = 0
            else:
                last_number = 0

            self.reference = f"ADM-{year}-{last_number + 1:05d}"

        super().save(*args, **kwargs)