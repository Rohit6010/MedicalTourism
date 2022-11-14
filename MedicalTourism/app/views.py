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

#For web scraping using beautiful soup
from bs4 import BeautifulSoup
import requests

def index(request):
    return render(request, 'index.html')


