from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, update_session_auth_hash
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.db.models import Sum
from admissions.models import AdmissionApplication
from .models import User
from .utils import account_activation_token
from .forms import (
    ActivateAccountForm,
    SettingsPasswordChangeForm,
    SettingsEmailForm,
)

# Dashboard models
from students.models import Student
from teachers.models import Teacher
from parents.models import Parent
from academics.models import Class as SchoolClass
from fees.models import Fee


# =====================================================
# PUBLIC PAGES
# =====================================================

def home(request):
    return render(request, "accounts/home.html")


def about(request):
    return render(request, "accounts/about.html")


def features(request):
    return render(request, "accounts/features.html")


def contact(request):
    return render(request, "accounts/contact.html")


# =====================================================
# ADMIN DASHBOARD
# =====================================================

class DashboardPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard_placeholder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_parents = Parent.objects.count()
        total_classes = SchoolClass.objects.count()

        total_fees_due = Fee.objects.aggregate(total=Sum("amount_due"))["total"] or 0
        total_fees_paid = Fee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        outstanding_balance = total_fees_due - total_fees_paid
        pending_admissions = AdmissionApplication.objects.filter(status="PENDING").count()

        context.update({
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_parents": total_parents,
            "total_classes": total_classes,
            "total_fees_due": total_fees_due,
            "total_fees_paid": total_fees_paid,
            "outstanding_balance": outstanding_balance,
            "pending_admissions": pending_admissions,
        })

        return context


# =====================================================
# DASHBOARD ROUTER
# =====================================================

class DashboardRouterView(LoginRequiredMixin, View):
    def get(self, request):
        role = request.user.role

        if role == request.user.Role.STUDENT:
            return redirect("portal:student_dashboard")
        elif role == request.user.Role.TEACHER:
            return redirect("portal:teacher_dashboard")
        elif role == request.user.Role.PARENT:
            return redirect("portal:parent_dashboard")

        return redirect("dashboard")


# =====================================================
# HOME / ABOUT CLASS VIEWS
# =====================================================

class HomeView(TemplateView):
    template_name = "accounts/home.html"


class AboutView(TemplateView):
    template_name = "accounts/about.html"


# =====================================================
# ACCOUNT ACTIVATION
# =====================================================

class ActivateAccountView(View):
    template_name = "accounts/activate.html"

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        valid = user is not None and account_activation_token.check_token(user, token)
        form = ActivateAccountForm(user) if valid else None
        return render(request, self.template_name, {"valid": valid, "form": form})

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        valid = user is not None and account_activation_token.check_token(user, token)

        if not valid:
            return render(request, self.template_name, {"valid": False})

        form = ActivateAccountForm(user, request.POST)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect("dashboard_router")

        return render(request, self.template_name, {"valid": True, "form": form})


# =====================================================
# SETTINGS
# =====================================================

class SettingsView(LoginRequiredMixin, View):
    template_name = "accounts/settings.html"

    def get(self, request):
        password_form = SettingsPasswordChangeForm(request.user)
        email_form = SettingsEmailForm(instance=request.user)
        return render(request, self.template_name, {
            "password_form": password_form,
            "email_form": email_form,
        })

    def post(self, request):
        if "change_password" in request.POST:
            password_form = SettingsPasswordChangeForm(request.user, request.POST)
            email_form = SettingsEmailForm(instance=request.user)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully.")
                return redirect("settings")
        else:
            email_form = SettingsEmailForm(request.POST, instance=request.user)
            password_form = SettingsPasswordChangeForm(request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully.")
                return redirect("settings")

        return render(request, self.template_name, {
            "password_form": password_form,
            "email_form": email_form,
        })