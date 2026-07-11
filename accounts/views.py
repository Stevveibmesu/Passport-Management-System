from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from .forms import OfficerCreationForm
from .models import User


@login_required
@admin_required
def officer_list(request):
    officers = User.objects.all().order_by('username')
    return render(request, 'accounts/officer_list.html', {'officers': officers})


@login_required
@admin_required
def add_officer(request):
    if request.method == 'POST':
        form = OfficerCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role == 'admin':
                user.is_staff = True
            user.save()
            return redirect('officer_list')
    else:
        form = OfficerCreationForm()
    return render(request, 'accounts/officer_form.html', {'form': form})


@login_required
@admin_required
def toggle_officer_status(request, pk):
    officer = get_object_or_404(User, pk=pk)
    officer.is_active = not officer.is_active
    officer.save()
    return redirect('officer_list')