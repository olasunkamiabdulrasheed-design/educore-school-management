from django import forms
from .models import Announcement

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "body", "audience"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "body": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 5}),
            "audience": forms.Select(attrs={"class": INPUT_CLASSES}),
        }