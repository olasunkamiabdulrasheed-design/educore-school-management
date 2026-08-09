from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from accounts.mixins import AdminRequiredMixin
from academics.models import Class as SchoolClass
from students.models import Student
from .models import Fee
from .forms import FeeClassTermForm, FeeEntryForm


class EnterFeesView(AdminRequiredMixin, View):
    template_name = "fees/enter_fees.html"

    def get(self, request):
        class_id = request.GET.get("class_obj")
        term = request.GET.get("term")
        session = request.GET.get("session")

        class_term_form = FeeClassTermForm(request.GET or None)
        entry_form = None
        selected_class = None
        rows = []
        description = ""

        if class_id and term and session:
            selected_class = SchoolClass.objects.filter(pk=class_id).first()
            if selected_class:
                students = list(Student.objects.filter(class_name=selected_class))
                existing = {
                    f.student_id: f for f in Fee.objects.filter(
                        student__in=students, term=term, session=session
                    )
                }
                initial = {}
                for s in students:
                    fee = existing.get(s.id)
                    if fee:
                        initial[f"due_{s.id}"] = fee.amount_due
                        initial[f"paid_{s.id}"] = fee.amount_paid
                        description = fee.description or description

                entry_form = FeeEntryForm(students=students, initial=initial)

                for student in students:
                    rows.append({
                        "student": student,
                        "due_field": entry_form[f"due_{student.id}"],
                        "paid_field": entry_form[f"paid_{student.id}"],
                    })

        return render(request, self.template_name, {
            "class_term_form": class_term_form,
            "entry_form": entry_form,
            "selected_class": selected_class,
            "term": term,
            "session": session,
            "description": description,
            "rows": rows,
        })

    def post(self, request):
        class_id = request.POST.get("class_id")
        term = request.POST.get("term")
        session = request.POST.get("session")
        description = request.POST.get("description", "")
        selected_class = SchoolClass.objects.filter(pk=class_id).first()
        students = list(Student.objects.filter(class_name=selected_class))

        entry_form = FeeEntryForm(request.POST, students=students)

        if entry_form.is_valid():
            for student in students:
                due = entry_form.cleaned_data.get(f"due_{student.id}")
                paid = entry_form.cleaned_data.get(f"paid_{student.id}")
                if due is not None:
                    Fee.objects.update_or_create(
                        student=student, term=term, session=session,
                        defaults={"amount_due": due, "amount_paid": paid or 0, "description": description},
                    )
            return redirect(
                f"{reverse('fees:enter')}?class_obj={class_id}&term={term}&session={session}"
            )

        rows = []
        for student in students:
            rows.append({
                "student": student,
                "due_field": entry_form[f"due_{student.id}"],
                "paid_field": entry_form[f"paid_{student.id}"],
            })

        return render(request, self.template_name, {
            "class_term_form": FeeClassTermForm(initial={"class_obj": class_id, "term": term, "session": session}),
            "entry_form": entry_form,
            "selected_class": selected_class,
            "term": term,
            "session": session,
            "description": description,
            "rows": rows,
        })