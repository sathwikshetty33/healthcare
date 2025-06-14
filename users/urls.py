# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Patient URLs
    path('patient/signup/', views.patient_signup, name='patient_signup'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    
    # Doctor URLs
    path('doctor/signup/', views.doctor_signup, name='doctor_signup'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),
]