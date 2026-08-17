from django.urls import path
from . import views


app_name = "admissions"


urlpatterns = [
    path(
        "",
        views.AdmissionListView.as_view(),
        name="list"
    ),

    path(
        "<int:pk>/",
        views.AdmissionDetailView.as_view(),
        name="detail"
    ),

    path(
        "<int:pk>/status/<str:status>/",
        views.AdmissionStatusUpdateView.as_view(),
        name="status_update",
    ),

    path(
        "<int:pk>/edit/",
        views.AdmissionUpdateView.as_view(),
        name="edit"
    ),

    path("track/", views.TrackApplicationView.as_view(), name="track"),
    
    path("<int:pk>/approve/", views.AdmissionApproveView.as_view(), name="approve"),

    path(
        "apply/",
        views.AdmissionApplyView.as_view(),
        name="apply"
    ),

    path(
        "apply/success/",
        views.AdmissionApplySuccessView.as_view(),
        name="apply_success"
    ),
]