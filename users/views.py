# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Patient, Doctor, Address


def home(request):
    """Home page with login/signup options"""
    return render(request, 'home.html')


def patient_signup(request):
    """Patient signup view"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')
        
        # Address fields
        line1 = request.POST.get('line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'patient_signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'patient_signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'patient_signup.html')
        
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create address if provided
                address = None
                if line1 and city and state and pincode:
                    address = Address.objects.create(
                        line1=line1,
                        city=city,
                        state=state,
                        pincode=pincode
                    )
                
                # Create patient profile
                Patient.objects.create(
                    user=user, 
                    address=address,
                    profile_picture=profile_picture
                )
                
                messages.success(request, 'Patient account created successfully!')
                return redirect('patient_login')
                
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'patient_signup.html')


def doctor_signup(request):
    """Doctor signup view"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')
        
        # Address fields
        line1 = request.POST.get('line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'doctor_signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'doctor_signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'doctor_signup.html')
        
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create address if provided
                address = None
                if line1 and city and state and pincode:
                    address = Address.objects.create(
                        line1=line1,
                        city=city,
                        state=state,
                        pincode=pincode
                    )
                
                # Create doctor profile
                Doctor.objects.create(
                    user=user, 
                    address=address,
                    profile_picture=profile_picture
                )
                
                messages.success(request, 'Doctor account created successfully!')
                return redirect('doctor_login')
                
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'doctor_signup.html')


def patient_login(request):
    """Patient login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a patient
            try:
                patient = Patient.objects.get(user=user)
                login(request, user)
                return redirect('patient_dashboard')
            except Patient.DoesNotExist:
                messages.error(request, 'This account is not registered as a patient')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'patient_login.html')


def doctor_login(request):
    """Doctor login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a doctor
            try:
                doctor = Doctor.objects.get(user=user)
                login(request, user)
                return redirect('doctor_dashboard')
            except Doctor.DoesNotExist:
                messages.error(request, 'This account is not registered as a doctor')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'doctor_login.html')


@login_required
def patient_dashboard(request):
    """Patient dashboard view"""
    try:
        patient = Patient.objects.get(user=request.user)
        
        # Mock data for demonstration - replace with actual queries
        recent_appointments = [
            {
                'id': 1,
                'doctor_name': 'Dr. Smith',
                'date': '2024-06-15',
                'time': '10:30 AM',
                'status': 'Confirmed',
                'type': 'General Checkup'
            },
            {
                'id': 2,
                'doctor_name': 'Dr. Johnson',
                'date': '2024-06-20',
                'time': '2:00 PM',
                'status': 'Pending',
                'type': 'Cardiology'
            }
        ]
        
        medical_records = [
            {
                'id': 1,
                'date': '2024-06-10',
                'doctor': 'Dr. Smith',
                'diagnosis': 'Routine Checkup',
                'prescription': 'Multivitamins'
            },
            {
                'id': 2,
                'date': '2024-05-28',
                'doctor': 'Dr. Brown',
                'diagnosis': 'Mild Fever',
                'prescription': 'Paracetamol 500mg'
            }
        ]
        
        prescriptions = [
            {
                'id': 1,
                'medicine': 'Paracetamol 500mg',
                'dosage': 'Twice daily',
                'prescribed_by': 'Dr. Brown',
                'date': '2024-05-28',
                'status': 'Active'
            },
            {
                'id': 2,
                'medicine': 'Multivitamins',
                'dosage': 'Once daily',
                'prescribed_by': 'Dr. Smith',
                'date': '2024-06-10',
                'status': 'Active'
            }
        ]
        
        # Dashboard statistics
        stats = {
            'total_appointments': len(recent_appointments),
            'upcoming_appointments': len([a for a in recent_appointments if a['status'] == 'Confirmed']),
            'total_prescriptions': len(prescriptions),
            'active_prescriptions': len([p for p in prescriptions if p['status'] == 'Active'])
        }
        
        context = {
            'patient': patient,
            'user': request.user,
            'recent_appointments': recent_appointments[:3],  # Show only 3 recent
            'medical_records': medical_records[:3],  # Show only 3 recent
            'prescriptions': prescriptions[:3],  # Show only 3 recent
            'stats': stats,
        }
        return render(request, 'patient_dashboard.html', context)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found')
        return redirect('home')


@login_required
def doctor_dashboard(request):
    """Doctor dashboard view"""
    try:
        doctor = Doctor.objects.get(user=request.user)
        
        # Mock data for demonstration - replace with actual queries
        today_appointments = [
            {
                'id': 1,
                'patient_name': 'John Doe',
                'time': '10:30 AM',
                'type': 'General Checkup',
                'status': 'Confirmed'
            },
            {
                'id': 2,
                'patient_name': 'Jane Smith',
                'time': '2:00 PM',
                'type': 'Follow-up',
                'status': 'Confirmed'
            },
            {
                'id': 3,
                'patient_name': 'Mike Johnson',
                'time': '4:30 PM',
                'type': 'Consultation',
                'status': 'Pending'
            }
        ]
        
        recent_patients = [
            {
                'id': 1,
                'name': 'John Doe',
                'last_visit': '2024-06-14',
                'condition': 'Hypertension',
                'status': 'Under Treatment'
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'last_visit': '2024-06-13',
                'condition': 'Diabetes',
                'status': 'Stable'
            },
            {
                'id': 3,
                'name': 'Mike Johnson',
                'last_visit': '2024-06-12',
                'condition': 'Routine Checkup',
                'status': 'Healthy'
            }
        ]
        
        pending_prescriptions = [
            {
                'id': 1,
                'patient': 'John Doe',
                'medicine': 'Lisinopril 10mg',
                'date': '2024-06-14',
                'status': 'To be reviewed'
            },
            {
                'id': 2,
                'patient': 'Jane Smith',
                'medicine': 'Metformin 500mg',
                'date': '2024-06-13',
                'status': 'Active'
            }
        ]
        
        upcoming_appointments = [
            {
                'id': 4,
                'patient_name': 'Sarah Wilson',
                'date': '2024-06-15',
                'time': '9:00 AM',
                'type': 'Consultation'
            },
            {
                'id': 5,
                'patient_name': 'Robert Brown',
                'date': '2024-06-15',
                'time': '11:30 AM',
                'type': 'Follow-up'
            }
        ]
        
        # Dashboard statistics
        stats = {
            'today_appointments': len(today_appointments),
            'total_patients': len(recent_patients) + 15,  # Mock total
            'pending_reviews': len(pending_prescriptions),
            'completed_today': 2  # Mock completed appointments
        }
        
        context = {
            'doctor': doctor,
            'user': request.user,
            'today_appointments': today_appointments,
            'recent_patients': recent_patients[:5],  # Show only 5 recent
            'pending_prescriptions': pending_prescriptions,
            'upcoming_appointments': upcoming_appointments[:3],  # Show only 3 upcoming
            'stats': stats,
        }
        return render(request, 'doctor_dashboard.html', context)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found')
        return redirect('home')


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')