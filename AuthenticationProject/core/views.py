from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *

@login_required
def Home(request):
    return render(request, 'index.html')

def RegisterView(request):
    if request.method == 'POST':

        # Getting user inputs from frontend
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')

        # Check password length
        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters')

        if user_data_has_error:
            return redirect('register')

     
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        new_user.save()
        messages.success(request, 'Account created. Login now')
        return redirect('login')

    # If GET request, render the registration page
    return render(request, 'register.html')


def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect('login')

from django.core.mail import EmailMultiAlternatives

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            # Create password reset entry
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # Build reset link
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            
            # HTML email body
            html_content = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; background-color: #ffffff; color: #0b0b2d; text-align: center; padding: 20px;">

                    <p style="font-size: 12px; color: #666;">YOUR NEW PASSWORD</p>
                    <p style="font-size: 12px; color: #999; margin-bottom: 30px;">
                      IMPORTANT: This confirmation email has been generated automatically, so please do not reply.
                    </p>

                    <!-- You can replace this with your logo -->
                    <h2 style="font-weight: bold; font-size: 24px; margin: 20px 0;">Your new password</h2>
                     

                    <p style="font-size: 16px; margin: 10px 0;">Dear {user.username},</p>

                    <p style="font-size: 16px; margin: 20px 0;">
                      You have asked to reset your password.
                    </p>

                    <p style="font-size: 15px; margin-bottom: 30px;">
                      To do so, please use the link below:
                    </p>

                    <p>
                      <a href="{full_password_reset_url}" 
                         style="display: inline-block; background-color: #0b0b2d; color: white; 
                                padding: 14px 28px; text-decoration: none; font-size: 16px; 
                                border-radius: 6px; font-weight: bold;">
                        Change your password
                      </a>
                    </p>

                    <p style="font-size: 12px; color: #888; margin-top: 40px;">
                      If you didn’t request a password reset, you can safely ignore this email.
                    </p>

                  </body>
                </html>
                """

            # Send both plain text + HTML
            email_message = EmailMultiAlternatives(
                subject="Reset Your Password",
                body=html_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')
