from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PassportApplicationForm
from .models import PassportApplication


@login_required
def submit_application(request):
    if request.method == 'POST':
        form = PassportApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application_list')
        else:
            print(form.errors)
    else:
        form = PassportApplicationForm()

    return render(request, 'passports/submit.html', {'form': form})


@login_required
def application_list(request):
    query = request.GET.get('q', '').strip()
    applications = PassportApplication.objects.all().order_by('-submitted_at')
    if query:
        applications = applications.filter(
            Q(applicant__full_name__icontains=query) | Q(passport_number__icontains=query)
        )
    return render(request, 'passports/list.html', {'applications': applications, 'query': query})


@login_required
def update_status(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        application.status = new_status
        application.reviewed_by = request.user
        application.save()
        return redirect('application_list')

    return render(request, 'passports/update_status.html', {'application': application})