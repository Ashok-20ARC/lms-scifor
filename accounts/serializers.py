from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser as User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","email","role"]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","password","role"]
        extra_kwargs={"password":{"write_only":True}}

    def create(self,validated_data):
        user=User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role","student"),
            is_active=False
        )

        # General email verification

        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=token_generator.make_token(user)
        verify_url=f"https://localhost:8000/verify-email/{uid}/{token}/"

        send_mail(
            "verify Your Email",
            f"Click the link to verify your email:\n\n{verify_url}",
            "no-reply@lms.com",
            [user.email],
            fail_silently=False,
        )

        return user
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        email=data.get("email")
        password=data.get("password")
        user=authenticate(email=email,password=password)

        if not user:
            raise serializers.ValidationError("invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("Email not verified. Please check your inbox.")
        
        return user
    
class Tokenserializer(serializers.Serializer):
    refresh=serializers.CharField()
    access=serializers.CharField()

    def validate(self,data):
        user=self.context["user"]
        refresh=RefreshToken.for_user(user)
        return {"refresh":str(refresh),"access":str(refresh.access_token),}