from django import forms
from accounts.models import User
from .models import Student
from academics.models import Class as SchoolClass

INPUT_CLASS = "w-full px-3 py-2 rounded-lg border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-blue/40 focus:border-brand-blue"


class StudentCreateForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": INPUT_CLASS}))
    # password field removed — account uses an unusable password until the person activates it via link

    admission_no = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    class_name = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    gender = forms.ChoiceField(
        choices=[("MALE", "Male"), ("FEMALE", "Female")],
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    guardian_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    guardian_phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_admission_no(self):
        admission_no = self.cleaned_data["admission_no"]
        if Student.objects.filter(admission_no=admission_no).exists():
            raise forms.ValidationError("Admission number already exists.")
        return admission_no

    def save(self):
        data = self.cleaned_data
        user = User.objects.create(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            role=User.Role.STUDENT,
        )
        user.set_unusable_password()
        user.save()

        student = Student.objects.create(
            user=user,
            admission_no=data["admission_no"],
            class_name=data["class_name"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            phone=data["phone"],
            address=data["address"],
            guardian_name=data["guardian_name"],
            guardian_phone=data["guardian_phone"],
        )
        return student


class StudentUpdateForm(forms.Form):
    """Edits an existing Student + their linked User. No username/password here on purpose —
    changing login credentials is a separate, more sensitive action."""

    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": INPUT_CLASS}))

    admission_no = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    class_name = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    gender = forms.ChoiceField(
        choices=[("MALE", "Male"), ("FEMALE", "Female")],
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    guardian_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    guardian_phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    status = forms.ChoiceField(choices=Student.Status.choices, widget=forms.Select(attrs={"class": INPUT_CLASS}))

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)

    def clean_admission_no(self):
        admission_no = self.cleaned_data["admission_no"]
        qs = Student.objects.filter(admission_no=admission_no).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Admission number already exists.")
        return admission_no

    def save(self):
        data = self.cleaned_data
        user = self.instance.user
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.save()

        student = self.instance
        student.admission_no = data["admission_no"]
        student.class_name = data["class_name"]
        student.gender = data["gender"]
        student.date_of_birth = data["date_of_birth"]
        student.phone = data["phone"]
        student.address = data["address"]
        student.guardian_name = data["guardian_name"]
        student.guardian_phone = data["guardian_phone"]
        student.status = data["status"]
        student.save()
        return student