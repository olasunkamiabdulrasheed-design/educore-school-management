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
from django.urls import reverse
from django.shortcuts import get_object_or_404
from accounts.utils import build_activation_link
from accounts.models import User
from students.models import Student
from .forms import AdmissionApplicationForm, AdmissionApproveForm


from .forms import AdmissionApplicationForm, AdmissionApproveForm, TrackApplicationForm


from django.conf import settings
from .utils import send_admission_email

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


            recipient = application.email or application.guardian_email
            if recipient:
                send_admission_email(
                subject="Admission Application Update — EduCore",
                template_name="admissions/emails/admission_rejected.html",
                context={"application": application},
                recipient_list=[recipient],
            )
                
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
            application = form.save()

            review_url = request.build_absolute_uri(
                reverse("admissions:detail", kwargs={"pk": application.pk})
            )

            # Send email to admin
            send_admission_email(
                subject=f"New Admission Application — {application.reference}",
                template_name="admissions/emails/new_application_admin.html",
                context={"application": application, "review_url": review_url},
                recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            )

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


class AdmissionApproveView(AdminRequiredMixin, View):
    template_name = "admissions/admission_confirm.html"

    def get(self, request, pk):
        application = get_object_or_404(AdmissionApplication, pk=pk)
        if application.status == AdmissionApplication.Status.APPROVED:
            messages.info(request, "This application has already been approved.")
            return redirect("admissions:detail", pk=pk)

        form = AdmissionApproveForm(initial={
            "class_obj": application.applying_for,
            "admission_no": application.reference.replace("ADM-", "STU") if application.reference else "",
        })
        return render(request, self.template_name, {"application": application, "form": form})

    def post(self, request, pk):
        application = get_object_or_404(AdmissionApplication, pk=pk)
        form = AdmissionApproveForm(request.POST)

        if form.is_valid():
            selected_class = form.cleaned_data["class_obj"]
            admission_no = form.cleaned_data["admission_no"]

            if Student.objects.filter(admission_no=admission_no).exists():
                form.add_error("admission_no", "This admission number is already in use.")
                return render(request, self.template_name, {"application": application, "form": form})

            base_username = f"{application.first_name}.{application.last_name}".lower().replace(" ", "")
            username = base_username
            suffix = 1
            while User.objects.filter(username=username).exists():
                suffix += 1
                username = f"{base_username}{suffix}"

            user = User.objects.create(
                username=username,
                first_name=application.first_name,
                last_name=application.last_name,
                email=application.email,
                role=User.Role.STUDENT,
            )
            user.set_unusable_password()
            user.save()

            student = Student.objects.create(
                user=user,
                admission_no=admission_no,
                class_name=selected_class,
                gender=application.gender,
                date_of_birth=application.date_of_birth,
                phone=application.phone,
                address=application.address,
                guardian_name=application.guardian_name,
                guardian_phone=application.guardian_phone,
            )

            application.status = AdmissionApplication.Status.APPROVED
            application.student = student
            application.save()

            activation_link = build_activation_link(request, user)

            recipient = application.email or application.guardian_email
            if recipient:
                send_admission_email(
                    subject="Your Admission Has Been Approved — EduCore",
                    template_name="admissions/emails/admission_approved.html",
                    context={"application": application, "activation_link": activation_link},
                    recipient_list=[recipient],
                )
            return render(request, "admissions/admission_enrolled.html", {
                "application": application,
                "student": student,
                "activation_link": activation_link,
            })

        return render(request, self.template_name, {"application": application, "form": form})



class TrackApplicationView(View):
    template_name = "admissions/track_application.html"

    def get(self, request):
        form = TrackApplicationForm()
        return render(request, self.template_name, {"form": form, "application": None})

    def post(self, request):
        form = TrackApplicationForm(request.POST)
        application = None

        if form.is_valid():
            reference = form.cleaned_data["reference"].strip().upper()
            phone = form.cleaned_data["phone"].strip()

            application = AdmissionApplication.objects.filter(
                reference__iexact=reference, guardian_phone=phone
            ).first()

            if not application:
                form.add_error(None, "No application found matching that reference and phone number.")

        return render(request, self.template_name, {"form": form, "application": application})