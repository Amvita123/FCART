from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from FCART_APP.services import send_otp_mail
from django.core.mail import send_mail
from FCART_APP.send_sms import sendsms, send_otp_call
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.utils.crypto import get_random_string


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            otp = generate_otp()

            if user.verify_through == 'Mobile_SMS':
                phone_number = user.phone_no
                sendsms(phone_number, otp)

            elif user.verify_through == 'Email':
                send_otp_mail(user.email, otp)

            elif user.verify_through == 'call':
                phone_number = user.phone_no
                send_otp_call(phone_number, otp)

            user.save()
            save_otp_in_session(request, otp)
            request.session['email'] = form.cleaned_data['email']
            send_otp_email(request, form.cleaned_data['email'], otp)
            messages.success(request, 'Registration Complete')
            return redirect('verify_otp')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


User = get_user_model()


def user_login(request):
    if request.method == 'POST':
        email_phone_no = request.POST['email_phone_no']
        password = request.POST.get('password')
        user = None
        if '@' in email_phone_no:
            try:
                user = User.objects.get(email=email_phone_no)
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
                return redirect('login')
        else:
            try:
                user = User.objects.get(phone_no=email_phone_no)
            except User.DoesNotExist:
                messages.error(request, 'User with this phone number does not exist.')
                return redirect('login')

        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {email_phone_no}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'User not found.')
    return render(request, 'login.html')


def generate_otp():
    return get_random_string(length=6, allowed_chars='0123456789')


def save_otp_in_session(request, otp):
    request.session['otp'] = otp


def send_otp_email(request, email, otp):
    try:
        subject = "OTP Verification"
        mail_message = f"Your OTP is {otp}. Please use it within the next 10 minutes."
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, mail_message, from_email, [email])
    except Exception as e:
        messages.error(request, f'Error sending email: {str(e)}')


def verify_otp(request):
    message = None
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get("email")
        if entered_otp == str(request.session.get('otp')):
            usr = User.objects.filter(email=email).first()
            if usr:
                usr.is_active = True
                usr.save()
                del request.session["email"]
                del request.session["otp"]
                messages.success(request, "OTP Verified Successfully!")
                return redirect('home')
            else:
                message = 'User not found.'
        else:
            message = 'Invalid OTP. Try again.'
    return render(request, 'verify_otp.html', {'message': message})


def resend_otp(request):
    if 'email' in request.session:
        email = request.session['email']
        otp = generate_otp()
        save_otp_in_session(request, otp)
        send_otp_email(request, email, otp)
        messages.success(request, 'OTP has been resent to your email.')
        return redirect('verify_otp')
    else:
        messages.error(request, "Session expired. Please request a new OTP.")
    return redirect('verify_otp')




