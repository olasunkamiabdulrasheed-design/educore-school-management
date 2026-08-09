from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from accounts.mixins import AdminRequiredMixin
from accounts.utils import build_activation_link
from .models import Parent
from .forms import ParentCreateForm, ParentUpdateForm


class ParentListView(AdminRequiredMixin, ListView):
    model = Parent
    template_name = "parents/parent_list.html"
    context_object_name = "parents"
    paginate_by = 20
    ordering = ["-id"]


class ParentDetailView(AdminRequiredMixin, DetailView):
    model = Parent
    template_name = "parents/parent_detail.html"
    context_object_name = "parent"


class ParentCreateView(AdminRequiredMixin, FormView):
    form_class = ParentCreateForm
    template_name = "parents/parent_form.html"

    def form_valid(self, form):
        parent = form.save()
        activation_link = build_activation_link(self.request, parent.user)
        return render(self.request, "parents/parent_created.html", {
            "parent": parent,
            "activation_link": activation_link,
        })


class ParentUpdateView(AdminRequiredMixin, UpdateView):
    model = Parent
    form_class = ParentUpdateForm
    template_name = "parents/parent_edit_form.html"
    success_url = reverse_lazy("parents:list")


class ParentDeleteView(AdminRequiredMixin, DeleteView):
    model = Parent
    template_name = "parents/parent_confirm_delete.html"
    success_url = reverse_lazy("parents:list")