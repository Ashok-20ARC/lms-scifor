from django.urls import path
from .views import signup_view,login_view,verify_email,RegisterView,LoginView,VerifyEmailView,UserProfileView

urlpatterns=[
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('verify-email/<uidb64>/<token>/',verify_email,name='verify_email'),
    path('api/register/',RegisterView.as_view(),name="register"),
    path('api/login/',LoginView.as_view(),name="login"),
    path('api/verify-email/<uidb64>/<token>/',VerifyEmailView.as_view(),name='verify-email'),
    path('api/profile/',UserProfileView.as_view(),name='user-profile'),
]