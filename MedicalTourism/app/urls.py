from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('handleSignin/', views.handleSignin, name="handleSignin"),
    path('signup/', views.signup, name="signup"),
    path('handleSignup/', views.handleSignup, name="handleSignup"),
    path('input/', views.input, name="input"),
    path('handleInput/', views.handleInput, name="handleInput"),
]