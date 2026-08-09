from django.urls import path
from .views import StudentDashboardView
from . import views

app_name = "portal"

urlpatterns = [
    path("student/", StudentDashboardView.as_view(), name="student_dashboard"),
    path("student/timetable/", views.StudentTimetableView.as_view(), name="student_timetable"),
    path("teacher/", views.TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("parent/", views.ParentDashboardView.as_view(), name="parent_dashboard"),
]