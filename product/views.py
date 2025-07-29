from django.shortcuts import render, redirect, get_object_or_404
from django.template import context
from .models import Estate, Category
from django.contrib.auth import login, logout, authenticate, get_user_model
from account.forms import RegisterForm, LoginForm
from account.models import MyUser, OTPCode
import random
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail


User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))



def index(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(
            request, 
            "main/index.html",
            context={
                'categories': categories,
                }
    )

def work_single(request):
    """Detail page"""
    return render(
            request, 
            "main/work-single.html"
    )

def all_announcenments(request):
    categories = Category.objects.all()
    estates = Estate.objects.all()
    return render(
            request, 
            "main/all_announcenments.html",
            context={
                'categories': categories,
                'estates': estates
                }
    )


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'autentification/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                code = generate_otp()
                OTPCode.objects.create(user=user, code=code)

                request.session['otp_user_id'] = user.id

                send_mail(
                    subject='Код подтверждения входа',
                    message=f'Ваш одноразовый код: {code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email]
                )
                return redirect('verify_otp')
            else:
                return render(request, 'autentification/login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = LoginForm()
    return render(request, 'autentification/login.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.session.get('otp_user_id')

        if not user_id:
            error = "Сессия истекла. Пожалуйста, войдите заново."
            return render(request, 'autentification/verify_otp.html', {'error': error})

        user = get_object_or_404(User, pk=user_id)

        if action == 'verify':
            otp_input = request.POST.get('otp', '').strip()
            try:
                otp_record = OTPCode.objects.filter(user=user, code=otp_input).latest('created_at')
            except OTPCode.DoesNotExist:
                otp_record = None

            if otp_record and not otp_record.is_expired():
                login(request, user)
                request.session.pop('otp_user_id', None)
                return redirect('index')
            else:
                error = "Неверный или просроченный код"
                return render(request, 'autentification/verify_otp.html', {'error': error})

        elif action == 'resend':
            code = generate_otp()
            OTPCode.objects.create(user=user, code=code)
            try:
                send_mail(
                    subject="Новый код подтверждения",
                    message=f"Ваш новый код: {code}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                message = "Новый код отправлен на почту"
                return render(request, 'autentification/verify_otp.html', {'message': message})
            except Exception as e:
                error = f"Ошибка при отправке письма: {e}"
                return render(request, 'autentification/verify_otp.html', {'error': error})

    else:
        return render(request, 'autentification/verify_otp.html')

def logout_view(request):
    logout(request)
    return redirect('index')
