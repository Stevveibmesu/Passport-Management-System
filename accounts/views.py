from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required
from .forms import OfficerCreationForm, OfficerEditForm
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
            messages.success(request, f"Officer '{user.username}' created successfully.")
            return redirect('officer_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = OfficerCreationForm()
    return render(request, 'accounts/officer_form.html', {'form': form})


@login_required
@admin_required
def edit_officer(request, pk):
    officer = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = OfficerEditForm(request.POST, instance=officer)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = (user.role == 'admin')
            user.save()
            messages.success(request, f"{user.username}'s account was updated.")
            return redirect('officer_list')
    else:
        form = OfficerEditForm(instance=officer)

    return render(request, 'accounts/officer_edit.html', {'form': form, 'officer': officer})


@login_required
@admin_required
def toggle_officer_status(request, pk):
    officer = get_object_or_404(User, pk=pk)
    officer.is_active = not officer.is_active
    officer.save()
    return redirect('officer_list')


@login_required
@admin_required
def delete_officer(request, pk):
    officer = get_object_or_404(User, pk=pk)

    if officer == request.user:
        messages.error(request, "You can't delete your own account while logged in.")
        return redirect('officer_list')

    if request.method == 'POST':
        officer.delete()
        messages.success(request, "Officer account deleted.")
        return redirect('officer_list')

    return render(request, 'accounts/officer_delete_confirm.html', {'officer': officer})