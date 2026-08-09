from django.db import models
from accounts.models import User
from academics.models import Class as SchoolClass


# CLASS_CHOICES = [
#     ("JSS 1A", "JSS 1A"), ("JSS 1B", "JSS 1B"), ("JSS 1C", "JSS 1C"),
#     ("JSS 2A", "JSS 2A"), ("JSS 2B", "JSS 2B"), ("JSS 2C", "JSS 2C"),
#     ("JSS 3A", "JSS 3A"), ("JSS 3B", "JSS 3B"), ("JSS 3C", "JSS 3C"),
#     ("SS 1A", "SS 1A"), ("SS 1B", "SS 1B"), ("SS 1C", "SS 1C"),
#     ("SS 2A", "SS 2A"), ("SS 2B", "SS 2B"), ("SS 2C", "SS 2C"),
#     ("SS 3A", "SS 3A"), ("SS 3B", "SS 3B"), ("SS 3C", "SS 3C"),
# ]
# not longer needed since i have a mdoel in my academic be a ForeignKey to the Class model.

class Student(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    admission_no = models.CharField(max_length=20, unique=True)

    # Old field (optional if you're migrating)
    # class_name = models.CharField(
    #     max_length=20,
    #     choices=CLASS_CHOICES
    # )
    # new field to replace the old class_name field, linking to the Class model


    
    # New relationship to the Class model
    class_name = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    gender = models.CharField(
        max_length=10,
        choices=[
            ("MALE", "Male"),
            ("FEMALE", "Female")
        ]
    )

    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    date_admitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username}"
            f" ({self.admission_no})"
        )