from django import forms
from .models import AdmissionApplication


INPUT_CLASSES = (
    "w-full px-4 py-3 rounded-xl border border-slate-200 "
    "bg-white text-slate-700 text-sm outline-none "
    "focus:ring-2 focus:ring-blue-500/20 "
    "focus:border-blue-500 transition"
)


class AdmissionApplicationForm(forms.ModelForm):

    class Meta:
        model = AdmissionApplication

        fields = [
            "first_name",
            "last_name",
            "other_names",
            "gender",
            "date_of_birth",
            "email",
            "phone",
            "address",
            "applying_for",
            "previous_school",
            "guardian_name",
            "guardian_phone",
            "guardian_email",
            "guardian_relationship",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Enter first name",
            }),

            "last_name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Enter last name",
            }),

            "other_names": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Other names (optional)",
            }),

            "gender": forms.Select(attrs={
                "class": INPUT_CLASSES,
            }),

            "date_of_birth": forms.DateInput(attrs={
                "class": INPUT_CLASSES,
                "type": "date",
            }),

            "email": forms.EmailInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Email address",
            }),

            "phone": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Phone number",
            }),

            "address": forms.Textarea(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Residential address",
                "rows": 3,
            }),

            "applying_for": forms.Select(attrs={
                "class": INPUT_CLASSES,
            }),

            "previous_school": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Previous school attended",
            }),

            "guardian_name": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Parent / Guardian full name",
            }),

            "guardian_phone": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Parent / Guardian phone",
            }),

            "guardian_email": forms.EmailInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Parent / Guardian email",
            }),

            "guardian_relationship": forms.TextInput(attrs={
                "class": INPUT_CLASSES,
                "placeholder": "e.g. Father, Mother, Guardian",
            }),
        }

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "other_names": "Other Names",
            "gender": "Gender",
            "date_of_birth": "Date of Birth",
            "email": "Email Address",
            "phone": "Phone Number",
            "address": "Residential Address",
            "applying_for": "Class Applying For",
            "previous_school": "Previous School",
            "guardian_name": "Parent / Guardian Name",
            "guardian_phone": "Parent / Guardian Phone",
            "guardian_email": "Parent / Guardian Email",
            "guardian_relationship": "Relationship",
        }


from academics.models import Class as SchoolClass


class AdmissionApproveForm(forms.Form):
    class_obj = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
        label="Assign to Class",
    )
    admission_no = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES}),
        label="Admission Number",
    )

from academics.models import Class as SchoolClass
class AdmissionApproveForm(forms.Form):
    class_obj = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
        label="Assign to Class",
    )
    admission_no = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES}),
        label="Admission Number",
    )



class TrackApplicationForm(forms.Form):
    reference = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "e.g. ADM-2026-00001"}),
        label="Application Reference",
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Guardian phone number"}),
        label="Phone Number",
    )