from accounts.mixins import AdminRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from .models import Student
from .forms import StudentCreateForm, StudentUpdateForm
from accounts.utils import build_activation_link
from django.shortcuts import render


class StudentListView(AdminRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    paginate_by = 20
    ordering = ["-date_admitted"]


class StudentDetailView(AdminRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"



class StudentCreateView(AdminRequiredMixin, FormView):
    form_class = StudentCreateForm
    template_name = "students/student_form.html"

    def form_valid(self, form):
        student = form.save()
        activation_link = build_activation_link(self.request, student.user)
        return render(self.request, "students/student_created.html", {
            "student": student,
            "activation_link": activation_link,
        })


class StudentUpdateView(AdminRequiredMixin, FormView):
    form_class = StudentUpdateForm
    template_name = "students/student_edit_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        s = self.student
        return {
            "first_name": s.user.first_name,
            "last_name": s.user.last_name,
            "email": s.user.email,
            "admission_no": s.admission_no,
            "class_name": s.class_name,
            "gender": s.gender,
            "date_of_birth": s.date_of_birth,
            "phone": s.phone,
            "address": s.address,
            "guardian_name": s.guardian_name,
            "guardian_phone": s.guardian_phone,
            "status": s.status,
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.student
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = self.student
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("students:detail", args=[self.student.pk]))


class StudentDeleteView(AdminRequiredMixin, View):
    """Deleting a student means deleting their linked User account too — the
    OneToOneField cascade takes care of removing the Student row automatically."""

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return self._render_confirm(request, student)

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.user.delete()  # cascades and deletes the Student row too
        return HttpResponseRedirect(reverse_lazy("students:list"))

    def _render_confirm(self, request, student):
        from django.shortcuts import render
        return render(request, "students/student_confirm_delete.html", {"student": student})