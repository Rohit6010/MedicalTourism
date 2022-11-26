from django.shortcuts import render, redirect
from django.http import HttpResponse
from sqlalchemy import null
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from googleapiclient.discovery import build

#For knowledge graph
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

#For api calling
import requests

def index(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'Auth/signin.html')


def signout(request):
    logout(request)
    return redirect('/')

def handleSignin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('/')
        else:
            messages.warning(request, "Invalid Credentials, please try again!")
            return HttpResponse("<h3>Invalid Credentials, please try again!</h3><br><a href='/signup'> Click here</a>")
    return render(request,'open.html')


def signup(request):
    return render(request, 'Auth/signup.html')


def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        name = request.POST['name']
        username = request.POST['uname']

        age = request.POST['age']
        phone = request.POST['phone']

        state = request.POST['state']
        city = request.POST['city']

        email = request.POST['email']
        password = request.POST['password']
        

        # Create the user in django table
        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        patient = Patient(p_id = myuser.id, name=name, age=age, phone=phone, state=state, city=city)
        patient.save()
        messages.success(request, " Your medical tourism account has been successfully created")
        return redirect('/')
    return render(request,'open.html')


def input(request):
    return render(request, 'input.html')


def handleInput(request):
    if request.method == "POST":

       return HttpResponse("Query submitted")