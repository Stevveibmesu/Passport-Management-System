from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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