from django import forms
from .models import Period, TimetableSlot
from academics.models import Class as SchoolClass, Subject
from .models import TimetableSlot, Period


INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ["number", "start_time", "end_time"]
        widgets = {
            "number": forms.NumberInput(attrs={"class": INPUT_CLASSES}),
            "start_time": forms.TimeInput(attrs={"class": INPUT_CLASSES, "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": INPUT_CLASSES, "type": "time"}),
        }



class TimetableClassForm(forms.Form):
    class_obj = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
        label="Class",
    )


class TimetableGridForm(forms.Form):
    """Dynamically builds one subject field per day per period."""
    def __init__(self, *args, periods=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.periods = periods or []
        days = TimetableSlot.Day.choices
        for day_value, day_label in days:
            for period in self.periods:
                field_name = f"subject_{day_value}_{period.id}"
                self.fields[field_name] = forms.ModelChoiceField(
                    queryset=Subject.objects.all(),
                    required=False,
                    widget=forms.Select(attrs={"class": INPUT_CLASSES}),
                )