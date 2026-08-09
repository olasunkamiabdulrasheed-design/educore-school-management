from django.shortcuts import render
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
# =====================================================
from django.contrib.auth import login
from django.contrib.auth.models import User as DjangoUser  # not used, just noting
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from .models import User
from .utils import account_activation_token
from .forms import ActivateAccountForm
# ====================================================
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import SettingsPasswordChangeForm, SettingsEmailForm


class DashboardPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard_placeholder.html"


# ====================================================================================================
# THIS WAS COMMENTED OUT IN THE ORIGINAL CODE, BUT I HAVE REWRITTEN IT BELOW FOR CLARITY AND FUNCTIONALITY. BY ANOTHER AI WHEN I ASKED IT TO REWRITE THE CODE. I HAVE NOT CHANGED ANYTHING IN THE CODE. I AM JUST ADDING THIS COMMENT FOR CLARITY.
# ============================================================================================
# class DashboardRouterView(LoginRequiredMixin, View):
#     def get(self, request):
#         role = request.user.role
#         if role == request.user.Role.STUDENT:
#             return redirect("portal:student_dashboard")
#         elif role == request.user.Role.TEACHER:
#             return redirect("portal:teacher_dashboard")
#         return redirect("dashboard")
# ====================================================================================================

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


# +++++++++++++++++++++++++++++++++++++++++++++++

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
                update_session_auth_hash(request, user)  # keeps them logged in after password change
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