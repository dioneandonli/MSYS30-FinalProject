"""
URL configuration for FinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # App Navigation
    path('dashboard/', views.dashboard_view, name='dashboard'), # This is the Home/Menu
    path('checkin/', views.check_in_patient, name='patient_check_in'),
    path('patientmanagement/', views.patient_management, name='patient_management'), # The Queue Dashboard
    
    # Logic: Call a specific patient
    path('call/<int:patient_id>/', views.call_next_patient, name='call_next_patient'),
    
    # Extras (Public Display & Details)
    path('queue-display/', views.queue_display_view, name='queue_display'),
    path('patient-details/', views.patient_details_view, name='patient_details'),
    
    # Logic: Mark current as complete (needed for the "Complete" button)
    path('complete/', views.complete_current_patient, name='complete_current_patient'),
]


