from accounts.mixins import AdminRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Class,Subject
from .forms import ClassForm, SubjectForm
from django.views.generic import DetailView

class ClassListView(AdminRequiredMixin, ListView):
    model = Class
    template_name = "academics/class_list.html"
    context_object_name = "classes"


class ClassCreateView(AdminRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = "academics/class_form.html"
    success_url = reverse_lazy("academics:list")


class ClassUpdateView(AdminRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "academics/class_form.html"
    success_url = reverse_lazy("academics:list")


class ClassDeleteView(AdminRequiredMixin, DeleteView):
    model = Class
    template_name = "academics/class_confirm_delete.html"
    success_url = reverse_lazy("academics:list")


class ClassDetailView(AdminRequiredMixin, DetailView):
    model = Class
    template_name = "academics/class_detail.html"
    context_object_name = "class_obj"


# =============================== SUBJECT VIEWS =====================================

class SubjectListView(AdminRequiredMixin, ListView):
    model = Subject
    template_name = "academics/Subjects/subject_list.html"
    context_object_name = "subjects"


class SubjectCreateView(AdminRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "academics/Subjects/subject_form.html"
    success_url = reverse_lazy("academics:subject_list")


class SubjectUpdateView(AdminRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "academics/Subjects/subject_form.html"
    success_url = reverse_lazy("academics:subject_list")


class SubjectDeleteView(AdminRequiredMixin, DeleteView):
    model = Subject
    template_name = "academics/Subjects/subject_confirm_delete.html"
    success_url = reverse_lazy("academics:subject_list")


