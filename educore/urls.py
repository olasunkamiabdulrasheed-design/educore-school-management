from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
    path("teachers/", include("teachers.urls")),
    path("", include("accounts.urls")),
    path("parents/", include("parents.urls")),
    path("classes/", include("academics.urls")),
    path("attendance/", include("attendance.urls")),
    path("exams/", include("examinations.urls")),
    path("fees/", include("fees.urls")),
    path("reports/", include("reports.urls")),
    path("announcements/", include("announcements.urls")),
    path("portal/", include("portal.urls")),
    path("timetable/", include("timetable.urls")),
    path("admissions/", include("admissions.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)