from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from examinations.models import Exam, Result, get_grade
from attendance.models import Attendance
from fees.models import Fee
from announcements.models import Announcement
from timetable.models import TimetableSlot, Period
from academics.models import Class as SchoolClass
from academics.models import Class as SchoolClass



class StudentDashboardView(LoginRequiredMixin, View):
    template_name = "portal/student_dashboard.html"

    def get(self, request):
        student = getattr(request.user, "student_profile", None)
        exams = Exam.objects.all()
        exam_id = request.GET.get("exam") or (exams.first().id if exams.exists() else None)

        selected_exam = None
        results_with_grades = []
        total_score = None
        average_score = None
        attendance_summary = None
        fee = None

        if student and exam_id:
            selected_exam = Exam.objects.filter(pk=exam_id).first()
            if selected_exam:
                results = Result.objects.filter(student=student, exam=selected_exam).select_related("subject")
                for result in results:
                    grade, remark = get_grade(result.score)
                    results_with_grades.append({
                        "subject": result.subject.name, "score": result.score,
                        "grade": grade, "remark": remark,
                    })
                if results:
                    total_score = sum(r.score for r in results)
                    average_score = total_score / len(results)

                attendance_qs = Attendance.objects.filter(
                    student=student, date__range=(selected_exam.start_date, selected_exam.end_date)
                )
                attendance_summary = {
                    "present": attendance_qs.filter(status=Attendance.Status.PRESENT).count(),
                    "absent": attendance_qs.filter(status=Attendance.Status.ABSENT).count(),
                    "late": attendance_qs.filter(status=Attendance.Status.LATE).count(),
                }

                fee = Fee.objects.filter(
                    student=student, term=selected_exam.term, session=selected_exam.session
                ).first()

        # Timetable — not tied to a specific exam, always shows current class schedule
        timetable_rows = []
        days = TimetableSlot.Day.choices
        if student and student.class_name:
            periods = list(Period.objects.all())
            slots = {
                (slot.day, slot.period_id): slot.subject
                for slot in TimetableSlot.objects.filter(class_obj=student.class_name)
            }
            for period in periods:
                row = {"period": period, "cells": []}
                for day_value, day_label in days:
                    subject = slots.get((day_value, period.id))
                    row["cells"].append(subject.name if subject else "—")
                timetable_rows.append(row)

        announcements = Announcement.objects.filter(
            audience__in=[Announcement.Audience.EVERYONE, Announcement.Audience.STUDENT]
        )[:5]

        return render(request, self.template_name, {
            "student": student,
            "exams": exams,
            "selected_exam": selected_exam,
            "results_with_grades": results_with_grades,
            "total_score": total_score,
            "average_score": average_score,
            "attendance_summary": attendance_summary,
            "fee": fee,
            "timetable_rows": timetable_rows,
            "days": days,
            "announcements": announcements,
        })



class ParentDashboardView(LoginRequiredMixin, View):
    template_name = "portal/parent_dashboard.html"

    def get(self, request):
        parent = getattr(request.user, "parent_profile", None)
        children = list(parent.children.all()) if parent else []

        student_id = request.GET.get("student")
        exam_id = request.GET.get("exam")

        selected_student = None
        exams = Exam.objects.all()
        selected_exam = None
        results_with_grades = []
        total_score = None
        average_score = None
        attendance_summary = None
        fee = None

        if student_id:
            selected_student = next((c for c in children if str(c.id) == student_id), None)

        if selected_student and exam_id:
            selected_exam = Exam.objects.filter(pk=exam_id).first()
            if selected_exam:
                results = Result.objects.filter(student=selected_student, exam=selected_exam).select_related("subject")
                for result in results:
                    grade, remark = get_grade(result.score)
                    results_with_grades.append({
                        "subject": result.subject.name, "score": result.score,
                        "grade": grade, "remark": remark,
                    })
                if results:
                    total_score = sum(r.score for r in results)
                    average_score = total_score / len(results)

                attendance_qs = Attendance.objects.filter(
                    student=selected_student, date__range=(selected_exam.start_date, selected_exam.end_date)
                )
                attendance_summary = {
                    "present": attendance_qs.filter(status=Attendance.Status.PRESENT).count(),
                    "absent": attendance_qs.filter(status=Attendance.Status.ABSENT).count(),
                    "late": attendance_qs.filter(status=Attendance.Status.LATE).count(),
                }

                fee = Fee.objects.filter(
                    student=selected_student, term=selected_exam.term, session=selected_exam.session
                ).first()

        announcements = Announcement.objects.filter(
            audience__in=[Announcement.Audience.EVERYONE, Announcement.Audience.PARENT]
        )[:5]

        return render(request, self.template_name, {
            "parent": parent, "children": children, "selected_student": selected_student,
            "exams": exams, "selected_exam": selected_exam, "results_with_grades": results_with_grades,
            "total_score": total_score, "average_score": average_score,
            "attendance_summary": attendance_summary, "fee": fee, "announcements": announcements,
        })

# ===============================


class TeacherDashboardView(LoginRequiredMixin, View):
    template_name = "portal/teacher_dashboard.html"

    def get(self, request):
        teacher = getattr(request.user, "teacher_profile", None)
        homeroom_class = None
        students = []

        if teacher:
            homeroom_class = SchoolClass.objects.filter(class_teacher=teacher).first()
            if homeroom_class:
                students = list(homeroom_class.students.all())

        announcements = Announcement.objects.filter(
            audience__in=[Announcement.Audience.EVERYONE, Announcement.Audience.TEACHER]
        )[:5]

        return render(request, self.template_name, {
            "teacher": teacher,
            "homeroom_class": homeroom_class,
            "students": students,
            "announcements": announcements,
        })
# ===================
class StudentTimetableView(LoginRequiredMixin, View):
    template_name = "portal/student_timetable.html"

    def get(self, request):
        student = getattr(request.user, "student_profile", None)
        timetable_rows = []
        days = TimetableSlot.Day.choices

        if student and student.class_name:
            periods = list(Period.objects.all())
            slots = {
                (slot.day, slot.period_id): slot.subject
                for slot in TimetableSlot.objects.filter(class_obj=student.class_name)
            }
            for period in periods:
                row = {"period": period, "cells": []}
                for day_value, day_label in days:
                    subject = slots.get((day_value, period.id))
                    row["cells"].append(subject.name if subject else "—")
                timetable_rows.append(row)

        return render(request, self.template_name, {
            "student": student,
            "timetable_rows": timetable_rows,
            "days": days,
        })

# -------------------------------------------




# ====================================================================================================
# THIS WAS COMMENTED OUT IN THE ORIGINAL CODE, BUT I HAVE REWRITTEN IT BELOW FOR CLARITY AND FUNCTIONALITY.
# ===================================================================================================



# class TeacherDashboardView(LoginRequiredMixin, View):
#     template_name = "portal/teacher_dashboard.html"

#     def get(self, request):
#         teacher = getattr(request.user, "teacher_profile", None)
#         my_class = None
#         students = []

#         if teacher:
#             my_class = SchoolClass.objects.filter(class_teacher=teacher).first()
#             if my_class:
#                 students = list(my_class.students.all())

#         announcements = Announcement.objects.filter(
#             audience__in=[Announcement.Audience.EVERYONE, Announcement.Audience.TEACHER]
#         )[:5]

#         return render(request, self.template_name, {
#             "teacher": teacher,
#             "my_class": my_class,
#             "students": students,
#             "announcements": announcements,
#         })

# ===========================================================================================