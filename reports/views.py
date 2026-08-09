from accounts.mixins import AdminRequiredMixin
from django.shortcuts import render
from django.views import View
from students.models import Student
from examinations.models import Exam, Result, get_grade
from attendance.models import Attendance
from fees.models import Fee


class StudentReportCardView(AdminRequiredMixin, View):
    template_name = "reports/student_report_card.html"

    def get(self, request):
        students = Student.objects.all()
        exams = Exam.objects.all()

        student_id = request.GET.get("student")
        exam_id = request.GET.get("exam")

        selected_student = None
        selected_exam = None
        results_with_grades = []
        total_score = None
        average_score = None
        attendance_summary = None
        fee = None
        class_position = None
        class_size = None

        if student_id and exam_id:
            selected_student = Student.objects.filter(pk=student_id).first()
            selected_exam = Exam.objects.filter(pk=exam_id).first()

            if selected_student and selected_exam:
                # Get this student's results, and attach a grade to each one
                results = Result.objects.filter(
                    student=selected_student, exam=selected_exam
                ).select_related("subject")

                for result in results:
                    grade, remark = get_grade(result.score)
                    results_with_grades.append({
                        "subject": result.subject.name,
                        "score": result.score,
                        "grade": grade,
                        "remark": remark,
                    })

                if results:
                    total_score = sum(r.score for r in results)
                    average_score = total_score / len(results)

                # Attendance during the exam's term window
                attendance_qs = Attendance.objects.filter(
                    student=selected_student,
                    date__range=(selected_exam.start_date, selected_exam.end_date),
                )
                attendance_summary = {
                    "present": attendance_qs.filter(status=Attendance.Status.PRESENT).count(),
                    "absent": attendance_qs.filter(status=Attendance.Status.ABSENT).count(),
                    "late": attendance_qs.filter(status=Attendance.Status.LATE).count(),
                }

                # Fee status for the matching term/session
                fee = Fee.objects.filter(
                    student=selected_student,
                    term=selected_exam.term,
                    session=selected_exam.session,
                ).first()

                # Class position: rank this student against classmates by total score
                if selected_student.class_name:
                    classmates = Student.objects.filter(class_name=selected_student.class_name)
                    totals = []
                    for classmate in classmates:
                        classmate_results = Result.objects.filter(student=classmate, exam=selected_exam)
                        if classmate_results:
                            classmate_total = sum(r.score for r in classmate_results)
                            totals.append((classmate.id, classmate_total))

                    totals.sort(key=lambda x: x[1], reverse=True)
                    class_size = len(totals)
                    for index, (sid, _) in enumerate(totals, start=1):
                        if sid == selected_student.id:
                            class_position = index
                            break

        return render(request, self.template_name, {
            "students": students,
            "exams": exams,
            "selected_student": selected_student,
            "selected_exam": selected_exam,
            "results_with_grades": results_with_grades,
            "total_score": total_score,
            "average_score": average_score,
            "attendance_summary": attendance_summary,
            "fee": fee,
            "class_position": class_position,
            "class_size": class_size,
        })