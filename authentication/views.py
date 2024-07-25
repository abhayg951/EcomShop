from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import login
# Create your views here.

def signup(request):
    if request.method == 'POST':
        # Getting the data from HTML form
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        re_password = request.POST.get('password_confirm')

        # Validate form data
        errors = []

        # Check for empty fields
        if not fname or not lname or not email or not phone_number or not password or not re_password:
            errors.append("All fields are required.")
        
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Enter a valid email address.")

        # Validate password
        if password != re_password:
            errors.append("Passwords do not match.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        
        # Validate phone number (assuming 10-digit format)
        if not phone_number.isdigit() or len(phone_number) != 10:
            errors.append("Enter a valid 10-digit phone number.")

        # If there are errors, send them back to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'authentication/signup.html')

        # Create the user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=fname,
                last_name=lname
            )
            user.save()
            messages.success(request, "User registered successfully.")
            return redirect('auth:login') 
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'authentication/signup.html')

    return render(request, 'authentication/signup.html')



def sign_in(request):
    print("function sign_in called")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            # login the user
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('store:home')
    return render(request, 'authentication/login.html')