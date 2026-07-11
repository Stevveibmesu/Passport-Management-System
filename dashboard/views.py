from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.decorators import admin_required
from applicants.models import Applicant
from passports.models import PassportApplication


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
@admin_required
def reports_view(request):
    User = get_user_model()
    stats = {
        'total_applicants': Applicant.objects.count(),
        'total_applications': PassportApplication.objects.count(),
        'pending': PassportApplication.objects.filter(status='pending').count(),
        'under_review': PassportApplication.objects.filter(status='under_review').count(),
        'approved': PassportApplication.objects.filter(status='approved').count(),
        'rejected': PassportApplication.objects.filter(status='rejected').count(),
        'total_officers': User.objects.count(),
    }
    return render(request, 'dashboard/reports.html', {'stats': stats})