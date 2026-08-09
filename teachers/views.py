from accounts.mixins import AdminRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .models import Teacher
from .forms import TeacherCreateForm, TeacherUpdateForm
from accounts.utils import build_activation_link
from django.shortcuts import render



class TeacherListView(AdminRequiredMixin, ListView):
    model = Teacher
    template_name = "teachers/teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 20
    ordering = ["-date_joined"]


class TeacherDetailView(AdminRequiredMixin, DetailView):
    model = Teacher
    template_name = "teachers/teacher_detail.html"
    context_object_name = "teacher"



class TeacherCreateView(AdminRequiredMixin, FormView):
    form_class = TeacherCreateForm
    template_name = "teachers/teacher_form.html"

    def form_valid(self, form):
        teacher = form.save()
        self.activation_link = build_activation_link(self.request, teacher.user)
        return render(self.request, "teachers/teacher_created.html", {
            "teacher": teacher,
            "activation_link": self.activation_link,
        })


class TeacherUpdateView(AdminRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherUpdateForm
    template_name = "teachers/teacher_edit_form.html"
    success_url = reverse_lazy("teachers:list")


class TeacherDeleteView(AdminRequiredMixin, DeleteView):
    model = Teacher
    template_name = "teachers/teacher_confirm_delete.html"
    success_url = reverse_lazy("teachers:list")