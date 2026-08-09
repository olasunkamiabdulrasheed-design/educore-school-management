from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [
    path("", views.ClassListView.as_view(), name="list"),
    path("add/", views.ClassCreateView.as_view(), name="add"),
    path("<int:pk>/", views.ClassDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.ClassUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ClassDeleteView.as_view(), name="delete"),

    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/add/", views.SubjectCreateView.as_view(), name="subject_add"),
    path("subjects/<int:pk>/edit/", views.SubjectUpdateView.as_view(), name="subject_edit"),
    path("subjects/<int:pk>/delete/", views.SubjectDeleteView.as_view(), name="subject_delete"),
]