from django.db import models
from academics.models import Class as SchoolClass, Subject


class Period(models.Model):
    number = models.PositiveIntegerField(unique=True)  # 1, 2, 3...
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Period {self.number} ({self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')})"


class TimetableSlot(models.Model):
    class Day(models.TextChoices):
        MONDAY = "MON", "Monday"
        TUESDAY = "TUE", "Tuesday"
        WEDNESDAY = "WED", "Wednesday"
        THURSDAY = "THU", "Thursday"
        FRIDAY = "FRI", "Friday"

    class_obj = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="timetable_slots")
    day = models.CharField(max_length=3, choices=Day.choices)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="slots")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("class_obj", "day", "period")
        ordering = ["day", "period__number"]

    def __str__(self):
        return f"{self.class_obj} — {self.get_day_display()} {self.period}: {self.subject}"