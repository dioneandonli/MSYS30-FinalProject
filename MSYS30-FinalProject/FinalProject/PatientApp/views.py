from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Patient

# --- Auth Views ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'PatientApp/signup.html', {'form': form, 'title': 'Sign-Up'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'PatientApp/login.html', {'form': form, 'title': 'Log-In'})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login') 

# --- Main Views ---

@login_required
def dashboard_view(request):
    """
    This is the Home Menu (Landing Page).
    """
    return render(request, 'PatientApp/home.html', {'title': 'Home'})

@login_required
def check_in_patient(request):
    """
    Handles patient registration.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob_str = request.POST.get('dob')
        contact = request.POST.get('contact')
        reason = request.POST.get('reason')

        if not name or not dob_str:
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                Patient.objects.create(
                    name=name,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    contact_info=contact,
                    reason_for_visit=reason,
                    status='Waiting'
                )
                messages.success(request, "Patient checked in successfully!")
                return redirect('patient_management')
            except Exception as e:
                messages.error(request, f"Error: {e}")

    return render(request, 'PatientApp/patient_checkin.html', {'title': 'Check-In'})

@login_required
def patient_management(request):
    """
    The Queue Management Dashboard.
    """
    currently_consulting = Patient.objects.filter(status='Consulting').first()
    waiting_patients = Patient.objects.filter(status='Waiting').order_by('timestamp')

    context = {
        'title': 'Queue Management',
        'currently_consulting': currently_consulting,
        'waiting_patients': waiting_patients,
        'current_date': datetime.now().strftime("%b. %d, %Y"),
    }
    return render(request, 'PatientApp/dashboard.html', context)

# --- Logic Views ---

@login_required
def call_next_patient(request, patient_id):
    """
    Calls a specific patient from the list.
    """
    # 1. Mark currently consulting patient as Completed (if any)
    current = Patient.objects.filter(status='Consulting').first()
    if current:
        current.status = 'Completed'
        current.save()

    # 2. Set the selected patient to Consulting
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.status = 'Consulting'
    patient.save()
    
    messages.success(request, f"Calling patient: {patient.name}")
    return redirect('patient_management')

@login_required
def complete_current_patient(request):
    """
    Marks the current patient as Completed without calling anyone else yet.
    """
    current = Patient.objects.filter(status='Consulting').first()
    if current:
        current.status = 'Completed'
        current.save()
        messages.info(request, "Consultation completed.")
    return redirect('patient_management')

# --- Extra Views ---

@login_required
def queue_display_view(request):
    current_patient = Patient.objects.filter(status='Consulting').first()
    waiting_patients = Patient.objects.filter(status='Waiting').order_by('timestamp')
    
    # Logic for "Next Patient" box (first in line)
    next_patient = waiting_patients.first()
    
    # List for the grid (excluding the one shown in "Next")
    if next_patient:
        grid_list = waiting_patients.exclude(id=next_patient.id)
    else:
        grid_list = waiting_patients

    context = {
        'title': 'Public Display',
        'current_patient': current_patient,
        'next_patient': next_patient,
        'queue_list': grid_list
    }
    return render(request, 'PatientApp/queue_display.html', context)

@login_required
def patient_details_view(request):
    return render(request, 'PatientApp/patient_details.html', {'title': 'Patient Details'})
