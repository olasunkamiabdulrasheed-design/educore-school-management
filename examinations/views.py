from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from accounts.mixins import AdminRequiredMixin, AdminOrTeacherRequiredMixin
from academics.models import Class as SchoolClass, Subject
from students.models import Student
from .models import Exam, Result, get_grade
from .forms import ExamClassForm, ResultsGridForm, ExamForm


class EnterResultsView(AdminOrTeacherRequiredMixin, View):
    template_name = "examinations/enter_results.html"

    def get(self, request):
        exam_id = request.GET.get("exam")
        class_id = request.GET.get("class_obj")

        if request.user.role == request.user.Role.TEACHER:
            teacher = getattr(request.user, "teacher_profile", None)
            class_queryset = SchoolClass.objects.filter(class_teacher=teacher)
        else:
            class_queryset = SchoolClass.objects.all()

        exam_class_form = ExamClassForm(request.GET or None)
        exam_class_form.fields["class_obj"].queryset = class_queryset

        grid_form = None
        selected_exam = None
        selected_class = None
        students = []
        subjects = []
        rows = []

        if exam_id and class_id:
            selected_exam = Exam.objects.filter(pk=exam_id).first()
            selected_class = class_queryset.filter(pk=class_id).first()
            if selected_exam and selected_class:
                subjects = list(selected_class.subjects.all())
                students = list(Student.objects.filter(class_name=selected_class))
                existing = {
                    (r.student_id, r.subject_id): r.score
                    for r in Result.objects.filter(exam=selected_exam, student__in=students)
                }
                initial = {
                    f"score_{s.id}_{sub.id}": existing.get((s.id, sub.id))
                    for s in students for sub in subjects
                }
                grid_form = ResultsGridForm(students=students, subjects=subjects, initial=initial)

                for student in students:
                    row_fields = [grid_form[f"score_{student.id}_{sub.id}"] for sub in subjects]
                    rows.append({"student": student, "fields": row_fields})

        return render(request, self.template_name, {
            "exam_class_form": exam_class_form,
            "grid_form": grid_form,
            "selected_exam": selected_exam,
            "selected_class": selected_class,
            "subjects": subjects,
            "rows": rows,
        })

    def post(self, request):
        exam_id = request.POST.get("exam_id")
        class_id = request.POST.get("class_id")

        if request.user.role == request.user.Role.TEACHER:
            teacher = getattr(request.user, "teacher_profile", None)
            class_queryset = SchoolClass.objects.filter(class_teacher=teacher)
        else:
            class_queryset = SchoolClass.objects.all()

        selected_exam = Exam.objects.filter(pk=exam_id).first()
        selected_class = class_queryset.filter(pk=class_id).first()
        students = list(Student.objects.filter(class_name=selected_class))
        subjects = list(selected_class.subjects.all()) if selected_class else []

        grid_form = ResultsGridForm(request.POST, students=students, subjects=subjects)

        if grid_form.is_valid():
            for student in students:
                for subject in subjects:
                    score = grid_form.cleaned_data.get(f"score_{student.id}_{subject.id}")
                    if score is not None:
                        Result.objects.update_or_create(
                            exam=selected_exam, student=student, subject=subject,
                            defaults={"score": score},
                        )
            return redirect(f"{reverse('examinations:enter')}?exam={exam_id}&class_obj={class_id}")

        rows = []
        for student in students:
            row_fields = [grid_form[f"score_{student.id}_{sub.id}"] for sub in subjects]
            rows.append({"student": student, "fields": row_fields})

        exam_class_form = ExamClassForm(initial={"exam": exam_id, "class_obj": class_id})
        exam_class_form.fields["class_obj"].queryset = class_queryset

        return render(request, self.template_name, {
            "exam_class_form": exam_class_form,
            "grid_form": grid_form,
            "selected_exam": selected_exam,
            "selected_class": selected_class,
            "subjects": subjects,
            "rows": rows,
        })


class ClassResultSheetView(AdminOrTeacherRequiredMixin, View):
    template_name = "examinations/class_result_sheet.html"

    def get(self, request):
        exam_id = request.GET.get("exam")
        class_id = request.GET.get("class_obj")

        if request.user.role == request.user.Role.TEACHER:
            teacher = getattr(request.user, "teacher_profile", None)
            class_queryset = SchoolClass.objects.filter(class_teacher=teacher)
        else:
            class_queryset = SchoolClass.objects.all()

        exams = Exam.objects.all()
        classes = class_queryset
        subjects = []

        selected_exam = None
        selected_class = None
        rows = []

        if exam_id and class_id:
            selected_exam = Exam.objects.filter(pk=exam_id).first()
            selected_class = class_queryset.filter(pk=class_id).first()
            if selected_exam and selected_class:
                subjects = list(selected_class.subjects.all())
                students = list(Student.objects.filter(class_name=selected_class))
                results = {
                    (r.student_id, r.subject_id): r.score
                    for r in Result.objects.filter(exam=selected_exam, student__in=students)
                }

                unranked_rows = []
                for student in students:
                    scores = [results.get((student.id, subj.id), "—") for subj in subjects]
                    raw_scores = [results.get((student.id, subj.id)) for subj in subjects]
                    total = sum(v for v in raw_scores if v is not None)
                    unranked_rows.append({"student": student, "scores": scores, "total": total})

                unranked_rows.sort(key=lambda r: r["total"], reverse=True)
                for index, row in enumerate(unranked_rows, start=1):
                    row["position"] = index
                rows = unranked_rows

        return render(request, self.template_name, {
            "exams": exams,
            "classes": classes,
            "subjects": subjects,
            "selected_exam": selected_exam,
            "selected_class": selected_class,
            "rows": rows,
        })


class ExamListView(AdminRequiredMixin, ListView):
    model = Exam
    template_name = "examinations/exam_list.html"
    context_object_name = "exams"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exams = Exam.objects.all().order_by("-session", "term")
        grouped = {}
        for exam in exams:
            grouped.setdefault(exam.session, []).append(exam)
        context["grouped_exams"] = grouped
        return context


class ExamCreateView(AdminRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = "examinations/exam_form.html"
    success_url = reverse_lazy("examinations:exam_list")


class ExamUpdateView(AdminRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = "examinations/exam_form.html"
    success_url = reverse_lazy("examinations:exam_list")


class ExamDeleteView(AdminRequiredMixin, DeleteView):
    model = Exam
    template_name = "examinations/exam_confirm_delete.html"
    success_url = reverse_lazy("examinations:exam_list")