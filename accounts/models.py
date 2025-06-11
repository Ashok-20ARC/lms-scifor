from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        email=self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('role','admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,password,**extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES=(
        ("student","Student"),
        ("staff","Staff"),
        ("admin","Admin"),
    )
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=30,blank=True)
    last_name=models.CharField(max_length=30,blank=True)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default="student")

    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=["first_name","last_name","role"]

    objects=CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
