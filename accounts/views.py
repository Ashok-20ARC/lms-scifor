<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import HttpResponse
from rest_framework import generics, status
=======
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,authenticate,login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import HttpResponse
from rest_framework import generics,status
>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< HEAD

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    TokenSerializer,
)
from django.contrib.auth import login as auth_login

User = get_user_model()


# ✅ Register + Send Email
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ✅ JWT Login + Active Check
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(token_data, status=status.HTTP_200_OK)


# ✅ Email Verification Link
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully. You can now login."})
        else:
            return Response({"message": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Protected Profile (JWT Required)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ✅ HTML-Based Signup Page (optional)
def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")

        user = User.objects.create_user(email=email, password=password, is_active=False)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')

        send_mail(
            'Verify your email',
=======
from .serializers import(RegisterSerializer,LoginSerializer,UserSerializer,Tokenserializer)

User=get_user_model()

class RegisterView(generics.CreateAPIView):  # creating inactive user and sending verification mail
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]

class LoginView(APIView):     # with JWT + Active Check
    permission_classes=[AllowAny]
    serializer_class=LoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data

        # Generate JWT tokens
        refresh=RefreshToken.for_user(user)
        token_data={
            "refresh":str(refresh),
            "access":str(refresh.access_token),
        }
        return Response(token_data,status=status.HTTP_200_OK)
    
class VerifyEmailView(APIView):
    permission_classes=[AllowAny]

    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user=None
        
        if user and token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return Response({"message":"Email verified Successfully. You can now login."})
        else:
            return Response({"message":"Invalid or expired link."},status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileView(generics.RetrieveAPIView):     # JWT Protected
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
         return self.request.user

def signup_view(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")
        
        user=User.objects.create_user(email=email,password=password,is_active=False)

        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=token_generator.make_token(user)
        verify_url=request.build_absolute_uri(f'/verify-email/{uid}/{token}/')

        send_mail(
            'verify your email',
>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
            f'Click the link to verify your email: {verify_url}',
            'no-reply@lms.com',
            [email],
            fail_silently=False,
        )
        return HttpResponse("Check your email to verify your account.")
<<<<<<< HEAD
    return render(request, 'signup.html')


# ✅ HTML-Based Email Verify
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and token_generator.check_token(user, token):
        user.is_active = True
=======
    return render(request,'signup.html')

def verify_email(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (User.DoesNotExist,ValueError,TypeError):
        user=None

    if user and token_generator.check_token(user,token):
        user.is_active=True
>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
        user.save()
        return HttpResponse('Email Verified: You can now log in.')
    else:
        return HttpResponse('Invalid or expired verification link.')
<<<<<<< HEAD


# ✅ HTML-Based Login Page (optional)
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            auth_login(request, user)
            return HttpResponse("Logged in successfully")
        else:
            return HttpResponse("Invalid login or email not verified.")
    return render(request, "login.html")


# ✅ Google Login (placeholder)
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # You can integrate with Google OAuth2 libraries here.
        return Response({"message": "Google login not yet implemented."})


# ✅ Password Reset Request
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_url = f"https://yourfrontend.com/reset-password/{uid}/{token}/"

        send_mail(
            "Reset your password",
            f"Click the link to reset your password:\n{reset_url}",
            "no-reply@lms.com",
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email sent."})


# ✅ Password Reset Confirm
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get("password")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link."}, status=400)

        if token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Password has been reset successfully."})
        else:
            return Response({"error": "Invalid or expired token."}, status=400)


# ✅ Resend Email Verification
class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"message": "Email is already verified."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = f"https://yourfrontend.com/verify-email/{uid}/{token}/"

        send_mail(
            "Verify your email",
            f"Click the link to verify your email:\n{verify_url}",
            "no-reply@lms.com",
            [email],
            fail_silently=False,
        )

        return Response({"message": "Verification email resent successfully."})
=======
    

def login_view(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)

        if user is not None and user.is_active:
            login(request,user)
            return HttpResponse("Logged in Successfully")
        else:
            return HttpResponse("Invalid login or email not verified.")
    return render(request,"login.html")
>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
