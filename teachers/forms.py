from django import forms
from accounts.models import User
from .models import Teacher

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class TeacherCreateForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": INPUT_CLASSES}))
    # password field removed — account uses an unusable password until activated

    subject_specialization = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    qualification = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    gender = forms.ChoiceField(choices=[("MALE", "Male"), ("FEMALE", "Female")], widget=forms.Select(attrs={"class": INPUT_CLASSES}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def save(self):
        data = self.cleaned_data
        user = User.objects.create(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            role=User.Role.TEACHER,
        )
        user.set_unusable_password()
        user.save()

        teacher = Teacher.objects.create(
            user=user,
            subject_specialization=data["subject_specialization"],
            qualification=data["qualification"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            phone=data["phone"],
            address=data["address"],
        )
        return teacher


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            "subject_specialization", "qualification", "gender",
            "date_of_birth", "phone", "address", "status",
        ]
        widgets = {
            "subject_specialization": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "qualification": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "gender": forms.Select(attrs={"class": INPUT_CLASSES}),
            "date_of_birth": forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "address": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "status": forms.Select(attrs={"class": INPUT_CLASSES}),
        }