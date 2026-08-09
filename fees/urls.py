from django.urls import path
from .views import EnterFeesView

app_name = "fees"

urlpatterns = [
    path("enter/", EnterFeesView.as_view(), name="enter"),
]