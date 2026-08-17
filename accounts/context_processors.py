from admissions.models import AdmissionApplication


def pending_admissions(request):
    if request.user.is_authenticated and getattr(request.user, "role", None) == "ADMIN":
        count = AdmissionApplication.objects.filter(status="PENDING").count()
    else:
        count = 0
    return {"pending_admissions": count}