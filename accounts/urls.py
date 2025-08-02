from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    UserProfileView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ResendEmailVerificationView,
    ChangePasswordView,
    StaffListCreateAPIView,
    StaffDetailAPIView
)

urlpatterns = [

    # Core auth APIs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verify-email/', ResendEmailVerificationView.as_view(), name='resend-verification'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Password reset
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # Change password
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),

    # Staff
    path('staffs/',StaffListCreateAPIView.as_view(),name='staff-list-create'),
    path('staffs/<int:pk>/',StaffDetailAPIView.as_view(),name='staff-detail'),
]
