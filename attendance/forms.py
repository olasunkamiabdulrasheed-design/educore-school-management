from django import forms
from academics.models import Class as SchoolClass
from .models import Attendance

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"

class AttendanceDateClassForm(forms.Form):
    class_obj = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
        label="Class",
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}),
    )


class AttendanceMarkingForm(forms.Form):
    """Dynamically builds one status field per student passed in."""
    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.students = students or []
        for student in self.students:
            self.fields[f"status_{student.id}"] = forms.ChoiceField(
                choices=Attendance.Status.choices,
                widget=forms.Select(attrs={"class": INPUT_CLASSES}),
                label=str(student),
                initial=Attendance.Status.PRESENT,
            )