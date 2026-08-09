from django.urls import path
from .views import StudentReportCardView

app_name = "reports"

urlpatterns = [
    path("student/", StudentReportCardView.as_view(), name="student_card"),
]