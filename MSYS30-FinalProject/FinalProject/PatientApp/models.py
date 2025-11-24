# PatientApp/models.py

from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Patient ID") 
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    reason_for_visit = models.TextField(blank=True, null=True, verbose_name="Condition")
    
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Consulting', 'Consultation On-going'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Arrival Time")
    
    class Meta:
        ordering = ['timestamp'] 

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.patient_id:
            # Generate P-ID using the primary key
            self.patient_id = f"P-{self.pk:05d}"
            super().save(update_fields=['patient_id'])
