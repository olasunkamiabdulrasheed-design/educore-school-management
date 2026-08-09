from django.db import models
from students.models import Student

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"