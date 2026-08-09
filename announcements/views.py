from accounts.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Announcement
from .forms import AnnouncementForm


class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = "announcements/announcement_list.html"
    context_object_name = "announcements"

    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.ADMIN:
            return Announcement.objects.all()
        return Announcement.objects.filter(
            audience__in=[Announcement.Audience.EVERYONE, user.role]
        )


class AnnouncementCreateView(AdminRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"
    success_url = reverse_lazy("announcements:list")

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(AdminRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"
    success_url = reverse_lazy("announcements:list")


class AnnouncementDeleteView(AdminRequiredMixin, DeleteView):
    model = Announcement
    template_name = "announcements/announcement_confirm_delete.html"
    success_url = reverse_lazy("announcements:list")