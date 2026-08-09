from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from accounts.mixins import AdminOrTeacherRequiredMixin
from academics.models import Class as SchoolClass
from students.models import Student
from .models import Attendance
from .forms import AttendanceDateClassForm, AttendanceMarkingForm


class MarkAttendanceView(AdminOrTeacherRequiredMixin, View):
    template_name = "attendance/mark_attendance.html"

    def get(self, request):
        class_id = request.GET.get("class_obj")
        date = request.GET.get("date")

        if request.user.role == request.user.Role.TEACHER:
            teacher = getattr(request.user, "teacher_profile", None)
            class_queryset = SchoolClass.objects.filter(class_teacher=teacher)
        else:
            class_queryset = SchoolClass.objects.all()

        date_form = AttendanceDateClassForm(request.GET or None)
        date_form.fields["class_obj"].queryset = class_queryset

        marking_form = None
        selected_class = None

        if class_id and date:
            selected_class = class_queryset.filter(pk=class_id).first()
            if selected_class:
                students = Student.objects.filter(class_name=selected_class)
                existing = {
                    a.student_id: a.status
                    for a in Attendance.objects.filter(student__in=students, date=date)
                }
                initial = {
                    f"status_{s.id}": existing.get(s.id, Attendance.Status.PRESENT)
                    for s in students
                }
                marking_form = AttendanceMarkingForm(students=students, initial=initial)

        return render(request, self.template_name, {
            "date_form": date_form,
            "marking_form": marking_form,
            "selected_class": selected_class,
            "date": date,
        })

    def post(self, request):
        class_id = request.POST.get("class_id")
        date = request.POST.get("date")

        if request.user.role == request.user.Role.TEACHER:
            teacher = getattr(request.user, "teacher_profile", None)
            class_queryset = SchoolClass.objects.filter(class_teacher=teacher)
        else:
            class_queryset = SchoolClass.objects.all()

        selected_class = class_queryset.filter(pk=class_id).first()
        students = Student.objects.filter(class_name=selected_class)

        marking_form = AttendanceMarkingForm(request.POST, students=students)
        if marking_form.is_valid():
            for student in students:
                status = marking_form.cleaned_data[f"status_{student.id}"]
                Attendance.objects.update_or_create(
                    student=student, date=date,
                    defaults={"status": status},
                )
            return redirect(f"{reverse('attendance:mark')}?class_obj={class_id}&date={date}")

        date_form = AttendanceDateClassForm(initial={"class_obj": class_id, "date": date})
        date_form.fields["class_obj"].queryset = class_queryset

        return render(request, self.template_name, {
            "date_form": date_form,
            "marking_form": marking_form,
            "selected_class": selected_class,
            "date": date,
        })