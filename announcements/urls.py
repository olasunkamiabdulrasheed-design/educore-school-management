from django.urls import path
from . import views

app_name = "announcements"

urlpatterns = [
    path("", views.AnnouncementListView.as_view(), name="list"),
    path("add/", views.AnnouncementCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.AnnouncementUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AnnouncementDeleteView.as_view(), name="delete"),
]