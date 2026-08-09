from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.DashboardPlaceholderView.as_view(), name="dashboard"),
    path("dashboard-router/", views.DashboardRouterView.as_view(), name="dashboard_router"),
    path("activate/<uidb64>/<token>/", views.ActivateAccountView.as_view(), name="activate"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    
]