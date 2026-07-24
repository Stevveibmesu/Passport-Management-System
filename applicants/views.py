from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import admin_required
from .forms import ApplicantForm
from .models import Applicant


@login_required
def register_applicant(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.registered_by = request.user
            applicant.save()
            return redirect('applicant_list')
        else:
            print(form.errors)
    else:
        form = ApplicantForm()

    return render(request, 'applicants/register.html', {'form': form})


@login_required
def applicant_list(request):
    query = request.GET.get('q', '').strip()
    applicants = Applicant.objects.all().order_by('-created_at')
    if query:
        applicants = applicants.filter(
            Q(full_name__icontains=query) | Q(national_id_number__icontains=query)
        )
    return render(request, 'applicants/list.html', {'applicants': applicants, 'query': query})


@login_required
@admin_required
def delete_applicant(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)

    if request.method == 'POST':
        name = applicant.full_name
        applicant.delete()
        messages.success(request, f"{name} and all their applications were deleted.")
        return redirect('applicant_list')

    return render(request, 'applicants/delete_confirm.html', {'applicant': applicant})