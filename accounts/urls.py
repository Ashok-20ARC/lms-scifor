from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('verify-email/<uidb64>/<token>/',views.verify_email,name='verify_email')
]