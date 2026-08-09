from django import forms
from .models import Class, Subject

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ["name", "level", "class_teacher", "subjects"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "level": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "class_teacher": forms.Select(attrs={"class": INPUT_CLASSES}),
            "subjects": forms.SelectMultiple(attrs={"class": INPUT_CLASSES}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "code": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }