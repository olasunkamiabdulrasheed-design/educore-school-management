from django import forms
from academics.models import Class as SchoolClass
from .models import Fee

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class FeeClassTermForm(forms.Form):
    class_obj = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
        label="Class",
    )
    term = forms.ChoiceField(
        choices=Fee.Term.choices,
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
    )
    session = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "e.g. 2026/2027"}),
    )

    description = forms.CharField(
    max_length=255, required=False,
    widget=forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "e.g. Tuition, Books, Sports Levy"}),
    )


class FeeEntryForm(forms.Form):
    """Dynamically builds amount_due + amount_paid fields per student."""
    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.students = students or []
        for student in self.students:
            self.fields[f"due_{student.id}"] = forms.DecimalField(
                max_digits=10, decimal_places=2, required=False,
                widget=forms.NumberInput(attrs={"class": INPUT_CLASSES, "step": "0.01"}),
                label=f"{student} — Amount Due",
            )
            self.fields[f"paid_{student.id}"] = forms.DecimalField(
                max_digits=10, decimal_places=2, required=False,
                widget=forms.NumberInput(attrs={"class": INPUT_CLASSES, "step": "0.01"}),
                label=f"{student} — Amount Paid",
            )