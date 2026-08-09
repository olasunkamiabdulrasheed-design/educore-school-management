from django.urls import path
from . import views
from .views import (
    EnterResultsView, ExamListView, ExamCreateView, ExamUpdateView, ExamDeleteView,
)

app_name = "examinations"

urlpatterns = [
    path("enter/", EnterResultsView.as_view(), name="enter"),
    path("", ExamListView.as_view(), name="exam_list"),
    path("add/", ExamCreateView.as_view(), name="exam_add"),
    path("<int:pk>/edit/", ExamUpdateView.as_view(), name="exam_edit"),
    path("<int:pk>/delete/", ExamDeleteView.as_view(), name="exam_delete"),
    path("class-results/", views.ClassResultSheetView.as_view(), name="class_results"),
]