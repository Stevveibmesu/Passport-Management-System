from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import admin_required
from .forms import PassportApplicationForm, AppointmentForm, DocumentForm
from .models import PassportApplication, Payment, Appointment, Document, Notification


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

        Notification.objects.create(
            application=application,
            message=f"Application status changed to {application.get_status_display()}."
        )

        return redirect('application_list')

    return render(request, 'passports/update_status.html', {'application': application})


@login_required
def record_payment(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)
    payment, created = Payment.objects.get_or_create(application=application)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            payment.amount = amount
        if request.POST.get('mark_paid'):
            payment.status = 'paid'
            payment.recorded_by = request.user
        else:
            payment.status = 'unpaid'
        payment.save()

        if payment.status == 'paid':
            Notification.objects.create(
                application=application,
                message=f"Payment of KES {payment.amount} received. Receipt: {payment.receipt_number}."
            )

        return redirect('application_list')

    return render(request, 'passports/payment.html', {'application': application, 'payment': payment})


@login_required
def schedule_appointment(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.application = application
            appointment.scheduled_by = request.user
            appointment.save()

            Notification.objects.create(
                application=application,
                message=f"{appointment.get_purpose_display()} appointment scheduled for {appointment.appointment_date} at {appointment.appointment_time}."
            )

            return redirect('appointment_list', pk=application.pk)
    else:
        form = AppointmentForm()

    appointments = application.appointments.all().order_by('-appointment_date')
    return render(request, 'passports/appointment_form.html', {
        'form': form, 'application': application, 'appointments': appointments
    })


@login_required
def appointment_list(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)
    appointments = application.appointments.all().order_by('-appointment_date')
    return render(request, 'passports/appointment_list.html', {
        'application': application, 'appointments': appointments
    })


@login_required
def update_appointment_status(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    if request.method == 'POST':
        appointment.status = request.POST.get('status')
        appointment.save()
    return redirect('appointment_list', pk=appointment.application.pk)


@login_required
def document_list(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            return redirect('document_list', pk=application.pk)
    else:
        form = DocumentForm()

    documents = application.documents.all().order_by('-uploaded_at')
    return render(request, 'passports/document_list.html', {
        'application': application, 'documents': documents, 'form': form
    })


@login_required
def verify_document(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    if request.method == 'POST':
        document.is_verified = not document.is_verified
        document.verified_by = request.user if document.is_verified else None
        document.save()

        if document.is_verified:
            Notification.objects.create(
                application=document.application,
                message=f"{document.get_document_type_display()} has been verified."
            )

    return redirect('document_list', pk=document.application.pk)


@login_required
def notification_list(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)
    notifications = application.notifications.all()
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'passports/notification_list.html', {
        'application': application, 'notifications': notifications
    })


@login_required
@admin_required
def delete_application(request, pk):
    application = get_object_or_404(PassportApplication, pk=pk)

    if request.method == 'POST':
        applicant_name = application.applicant.full_name
        application.delete()
        messages.success(request, f"Application for {applicant_name} was deleted.")
        return redirect('application_list')

    return render(request, 'passports/delete_confirm.html', {'application': application})