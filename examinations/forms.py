from django import forms
from academics.models import Class as SchoolClass, Subject
from students.models import Student
from .models import Exam, Result

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class ExamClassForm(forms.Form):
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
    )
    class_obj = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
        label="Class",
    )


class ResultsGridForm(forms.Form):
    """Dynamically builds one score field per student per subject."""
    def __init__(self, *args, students=None, subjects=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.students = students or []
        self.subjects = subjects or []
        for student in self.students:
            for subject in self.subjects:
                field_name = f"score_{student.id}_{subject.id}"
                self.fields[field_name] = forms.DecimalField(
                    max_digits=5, decimal_places=2,
                    required=False,
                    widget=forms.NumberInput(attrs={
                        "class": INPUT_CLASSES, "step": "0.01", "min": "0", "max": "100"
                    }),
                )


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["name", "term", "session", "start_date", "end_date"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "term": forms.Select(attrs={"class": INPUT_CLASSES}),
            "session": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "start_date": forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}),
        }