from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Patient
from datetime import datetime

def patient_management(request):
    currently_consulting = Patient.objects.filter(status='Consulting').order_by('timestamp').first()

    waiting_patients = Patient.objects.filter(status='Waiting').order_by('timestamp')

    context = {
        'currently_consulting': currently_consulting,
        'waiting_patients': waiting_patients,
        'current_date': datetime.now().strftime("%b. %d, %Y"),
        'current_time': datetime.now().strftime("%I:%M:%S %p"),
    }
    return render(request, 'PatientApp/patientmanagement.html', context)


# Call Next Patient view
def call_next_patient(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id, status='Waiting')
        patient.status = 'Consulting'
        patient.save()
    except Patient.DoesNotExist:
        pass 
    
    return redirect(reverse('patient_management'))

def check_in_patient(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        date_of_birth_str = request.POST.get('date_of_birth')
        contact_info = request.POST.get('contact_info')
        reason_for_visit = request.POST.get('reason_for_visit')
        
        if not name or not date_of_birth_str or not gender:
            return render(request, 'PatientApp/checkinpatient.html', {'error': 'Please fill in all required fields.'})

        try:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            
            Patient.objects.create(
                name=name,
                gender=gender,
                date_of_birth=date_of_birth,
                contact_info=contact_info,
                reason_for_visit=reason_for_visit,
            )
            
            return redirect(reverse('patient_management'))
            
        except Exception as e:

            return render(request, 'PatientApp/checkinpatient.html', {'error': f'An error occurred: {e}'})
            
    # GET request: Display the empty form
    return render(request, 'PatientApp/checkinpatient.html')
