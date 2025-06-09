from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,authenticate,login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import HttpResponse

User=get_user_model()

def signup_view(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=User.objects.create_user(email=email,password=password)
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=token_generator.make_token(user)
        verify_url=request.build_absolute_uri(f'/verify-email/{uid}/{token}/')

        send_mail(
            'verify your email',
            f'Click the link to verify your email: {verify_url}',
            'no-reply@lms.com',
            [email],
            fail_silently=False,
        )
        return HttpResponse("Check your email to verify your account.")
    return render(request,'signup.html')

def verify_email(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (User.DoesNotExist,ValueError,TypeError):
        user=None

    if user and token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return HttpResponse('Email Verified: You can now log in.')
    else:
        return HttpResponse('Invalid or expired verification link.')
    

def login_view(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)

        if user is not None and user.is_active:
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid login or email not verified.")
    return render(request,"login.html")