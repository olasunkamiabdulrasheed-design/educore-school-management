from django.db import models
from students.models import Student
from academics.models import Subject
from django.db import models
from students.models import Student


class Exam(models.Model):
    class Term(models.TextChoices):
        FIRST = "FIRST", "First Term"
        SECOND = "SECOND", "Second Term"
        THIRD = "THIRD", "Third Term"

    name = models.CharField(max_length=100)              # e.g. "First Term Examination"
    term = models.CharField(max_length=10, choices=Term.choices)
    session = models.CharField(max_length=20)             # e.g. "2026/2027"
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} — {self.get_term_display()} {self.session}"


class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="results")
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("exam", "student", "subject")
        ordering = ["student", "subject"]

    def __str__(self):
        return f"{self.student} — {self.subject} — {self.exam}: {self.score}"

def get_grade(score):
    score = float(score)
    if score >= 70:
        return ("A", "Excellent")
    elif score >= 60:
        return ("B", "Very Good")
    elif score >= 50:
        return ("C", "Good")
    elif score >= 45:
        return ("D", "Fair")
    elif score >= 40:
        return ("E", "Pass")
    else:
        return ("F", "Fail")



