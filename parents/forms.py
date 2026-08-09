from django import forms
from accounts.models import User
from students.models import Student
from .models import Parent

INPUT_CLASSES = "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class ParentCreateForm(forms.Form):
    # User/account fields
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": INPUT_CLASSES}))
    # password field removed — account uses an unusable password until the person activates it via link

    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    occupation = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    children = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": INPUT_CLASSES}),
        required=False,
    )

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
            role=User.Role.PARENT,
        )
        user.set_unusable_password()
        user.save()

        parent = Parent.objects.create(
            user=user,
            phone=data["phone"],
            address=data["address"],
            occupation=data["occupation"],
        )
        parent.children.set(data["children"])
        return parent


class ParentUpdateForm(forms.ModelForm):
    children = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": INPUT_CLASSES}),
        required=False,
    )

    class Meta:
        model = Parent
        fields = ["phone", "address", "occupation", "children"]
        widgets = {
            "phone": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "address": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "occupation": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }