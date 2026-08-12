from email.mime import application

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.mixins import AdminRequiredMixin
from .forms import AdmissionApplicationForm
from .models import AdmissionApplication


class AdmissionListView(AdminRequiredMixin, ListView):
    model = AdmissionApplication
    template_name = "admissions/admission_list.html"
    context_object_name = "applications"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        print("LOGGED USER:", request.user)
        print("USERNAME:", request.user.username)
        print("ROLE:", getattr(request.user, "role", None))
        print("AUTHENTICATED:", request.user.is_authenticated)

        return super().dispatch(request, *args, **kwargs)


class AdmissionDetailView(AdminRequiredMixin, DetailView):
    model = AdmissionApplication
    template_name = "admissions/admission_detail.html"
    context_object_name = "application"


class AdmissionStatusUpdateView(AdminRequiredMixin, View):

    def post(self, request, pk, status):
        application = AdmissionApplication.objects.get(pk=pk)

        print("STATUS RECEIVED:", status)
        print("STATUS BEFORE:", application.status)

        if status == "APPROVED":
            application.status = AdmissionApplication.Status.APPROVED
            application.save()

            print("STATUS AFTER APPROVE:", application.status)

            messages.success(
                request,
                "Admission application approved successfully! ✅"
            )

        elif status == "REJECTED":
            application.status = AdmissionApplication.Status.REJECTED
            application.save()

            print("STATUS AFTER REJECT:", application.status)

            messages.warning(
                request,
                "Admission application rejected."
            )

        return redirect(
            "admissions:detail",
            pk=application.pk
        )

class AdmissionUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = AdmissionApplication
    form_class = AdmissionApplicationForm
    template_name = "admissions/admission_form.html"

    def test_func(self):
        return getattr(self.request.user, "role", None) == "ADMIN"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Admission application updated successfully! ✅"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "admissions:detail",
            kwargs={"pk": self.object.pk}
        )


class AdmissionApplyView(View):
    template_name = "admissions/apply.html"

    def get(self, request):
        form = AdmissionApplicationForm()

        return render(request, self.template_name, {
            "form": form,
        })

    def post(self, request):
        form = AdmissionApplicationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your admission application has been submitted successfully! ✅"
            )

            return redirect("admissions:apply_success")

        return render(request, self.template_name, {
            "form": form,
        })


class AdmissionApplySuccessView(View):
    template_name = "admissions/apply_success.html"

    def get(self, request):
        return render(request, self.template_name)