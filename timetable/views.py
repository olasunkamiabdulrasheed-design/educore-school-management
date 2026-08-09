from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from accounts.mixins import AdminRequiredMixin
from academics.models import Class as SchoolClass
from .models import Period, TimetableSlot
from .forms import PeriodForm, TimetableClassForm, TimetableGridForm


class PeriodListView(AdminRequiredMixin, ListView):
    model = Period
    template_name = "timetable/period_list.html"
    context_object_name = "periods"


class PeriodCreateView(AdminRequiredMixin, CreateView):
    model = Period
    form_class = PeriodForm
    template_name = "timetable/period_form.html"
    success_url = reverse_lazy("timetable:period_list")

    def form_valid(self, form):
        messages.success(self.request, f'Period "{form.instance}" created successfully! ✅')
        return super().form_valid(form)


class PeriodUpdateView(AdminRequiredMixin, UpdateView):
    model = Period
    form_class = PeriodForm
    template_name = "timetable/period_form.html"
    success_url = reverse_lazy("timetable:period_list")

    def form_valid(self, form):
        messages.success(self.request, f'Period "{form.instance}" updated successfully! ✅')
        return super().form_valid(form)


class PeriodDeleteView(AdminRequiredMixin, DeleteView):
    model = Period
    template_name = "timetable/period_confirm_delete.html"
    success_url = reverse_lazy("timetable:period_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Period "{obj}" deleted successfully! ✅')
        return super().delete(request, *args, **kwargs)


class ManageTimetableView(AdminRequiredMixin, View):
    template_name = "timetable/manage_timetable.html"

    def get(self, request):
        class_id = request.GET.get("class_obj")
        class_form = TimetableClassForm(request.GET or None)
        grid_form = None
        selected_class = None
        periods = list(Period.objects.all())
        days = TimetableSlot.Day.choices
        rows = []

        if class_id:
            selected_class = SchoolClass.objects.filter(pk=class_id).first()
            if selected_class:
                existing = {
                    (slot.day, slot.period_id): slot.subject_id
                    for slot in TimetableSlot.objects.filter(class_obj=selected_class)
                }
                initial = {
                    f"subject_{day_value}_{period.id}": existing.get((day_value, period.id))
                    for day_value, _ in days for period in periods
                }
                grid_form = TimetableGridForm(periods=periods, initial=initial)

                for period in periods:
                    row_fields = []
                    for day_value, day_label in days:
                        field_name = f"subject_{day_value}_{period.id}"
                        row_fields.append(grid_form[field_name])
                    rows.append({"period": period, "fields": row_fields})

        return render(request, self.template_name, {
            "class_form": class_form,
            "grid_form": grid_form,
            "selected_class": selected_class,
            "periods": periods,
            "days": days,
            "rows": rows,
        })

    def post(self, request):
        class_id = request.POST.get("class_id")
        selected_class = SchoolClass.objects.filter(pk=class_id).first()
        periods = list(Period.objects.all())
        days = TimetableSlot.Day.choices

        grid_form = TimetableGridForm(request.POST, periods=periods)

        if grid_form.is_valid():
            saved_count = 0
            for day_value, _ in days:
                for period in periods:
                    field_name = f"subject_{day_value}_{period.id}"
                    subject = grid_form.cleaned_data.get(field_name)
                    if subject is not None:
                        TimetableSlot.objects.update_or_create(
                            class_obj=selected_class, day=day_value, period=period,
                            defaults={"subject": subject},
                        )
                        saved_count += 1
            
            messages.success(
                request, 
                f'Timetable for {selected_class.name} saved successfully! ✅ {saved_count} slots updated.'
            )
            return redirect(f"{reverse('timetable:manage')}?class_obj={class_id}")
        else:
            messages.error(
                request, 
                'Failed to save timetable. Please check the form for errors. ❌'
            )

        rows = []
        for period in periods:
            row_fields = []
            for day_value, day_label in days:
                field_name = f"subject_{day_value}_{period.id}"
                row_fields.append(grid_form[field_name])
            rows.append({"period": period, "fields": row_fields})

        return render(request, self.template_name, {
            "class_form": TimetableClassForm(initial={"class_obj": class_id}),
            "grid_form": grid_form,
            "selected_class": selected_class,
            "periods": periods,
            "days": days,
            "rows": rows,
        })