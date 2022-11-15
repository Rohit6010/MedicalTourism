from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('handleSignin/', views.handleSignin, name="handleSignin"),
    path('signup/', views.signup, name="signup"),
    path('handleSignup/', views.handleSignup, name="handleSignup"),
]