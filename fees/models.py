from django.db import models
from students.models import Student


# ========================== FEES MODEL ==========================

class Fee(models.Model):
    class Term(models.TextChoices):
        FIRST = "FIRST", "First Term"
        SECOND = "SECOND", "Second Term"
        THIRD = "THIRD", "Third Term"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees")
    term = models.CharField(max_length=10, choices=Term.choices)
    session = models.CharField(max_length=20)  # e.g. "2026/2027"
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=255, blank=True)  # e.g. "Tuition, Books, Sports Levy"

    class Meta:
        unique_together = ("student", "term", "session")
        ordering = ["-session", "term"]

    @property
    def balance(self):
        return self.amount_due - self.amount_paid

    @property
    def is_fully_paid(self):
        return self.amount_paid >= self.amount_due

    def __str__(self):
        return f"{self.student} — {self.get_term_display()} {self.session}: ₦{self.amount_paid}/{self.amount_due}"