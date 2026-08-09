from django.urls import path
from .views import MarkAttendanceView

app_name = "attendance"

urlpatterns = [
    path("mark/", MarkAttendanceView.as_view(), name="mark"),
]