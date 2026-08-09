from django.urls import path
from . import views

app_name = "timetable"

urlpatterns = [
    path("periods/", views.PeriodListView.as_view(), name="period_list"),
    path("periods/add/", views.PeriodCreateView.as_view(), name="period_add"),
    path("periods/<int:pk>/edit/", views.PeriodUpdateView.as_view(), name="period_edit"),
    path("periods/<int:pk>/delete/", views.PeriodDeleteView.as_view(), name="period_delete"),
    path("manage/", views.ManageTimetableView.as_view(), name="manage"),
    
]