from django.shortcuts import render, redirect
from django.http import HttpResponse
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
import googlemaps
import requests
import json

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


def graph(request):
    if request.method == "POST":
       disease = request.POST['disease']
       budget = request.POST['budget']
       city = request.POST['city']
       print(city)
 
       #Delete records of previous query from Temp_info table
       Temp_info.objects.all().delete()

       #Traverse knowledge graph to find locations where disease is treated with in budget.
       uri = "neo4j+s://644b1253.databases.neo4j.io" 
       user = "neo4j"
       password = "MCeuOS4sfD2RnrMZ3Qa3Q1on8NciRV_9ueu5Igu1eGA"
       app = App(uri, user, password)

       kg_id = Disease.objects.get(disease_name = disease).kg_id
       cities = app._returnCitiesUnderBudget(kg_id, budget)

       #Save city name and it's max treatment price temporarily in database
       for ind in range(len(cities[0])):
         info = Temp_info(city_info = cities[0][ind], price_info = cities[1][ind])
         info.save()


       print(cities[0])
       locations = '+'.join(cities[0])
       if len(locations) == 0:
         return render(request, "oops.html")

       locations = locations + "+" + city + "+" + disease
       return redirect("/mapModule/" + locations)


def mapModule(request, location):
    #Googlemaps
    maps_api_key = 'AIzaSyB4s3s2DGxNxc7Inl12jxHrExJIHoyZIrw'
    gmaps = googlemaps.Client(key=maps_api_key)


    #Delete records of previous query from Temp_info_1 table
    Temp_info_1.objects.all().delete()

    #Sorting locations based on distance using geolocation API and storing in pair
    locations = location.split('+')
    print(locations)

    pair = {}
    n = len(locations)
    for ind in range(n-2) :
        # Requires cities name
        src_city = locations[n-2]
        dest_city = locations[ind]
        my_dist = gmaps.distance_matrix(src_city, dest_city)['rows'][0]['elements'][0]

        # Printing the result
        print(locations[ind], my_dist['distance']['value'])

        #Storing result temporarily in database
        info = Temp_info_1(city = dest_city, distance = my_dist['distance']['text'], time = my_dist['duration']['text'])
        info.save()

        #add to dictionary
        pair[locations[ind]] = my_dist['distance']['value'] 


    #sort pair dictionary
    pair = sorted(pair.items(), key=lambda kv:(kv[1], kv[0]))

    count=0
    sortedLocs = ''
    print("Sorted pair : ")
    for ind in range(3):
        if ind < len(pair):
            sortedLocs +=  "+" + pair[ind][0]
            count += 1
            

    return redirect('/display/1+' + str(count) + sortedLocs + "+" + locations[n-1])



def displayPlaces(request, sortedloc):
    sortedLocs = sortedloc.split('+')

    display = int(sortedLocs[0])
    count = int(sortedLocs[1])

    # Locate Hospitals and Doctors using places API.
    disease = sortedLocs[-1]
    location = sortedLocs[display+1]

    #Getting price for requested location and deleting temporary objects
    price = Temp_info.objects.get(city_info = location).price_info
    
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Hospitals For {disease}%20in%20{location}&key=AIzaSyB4s3s2DGxNxc7Inl12jxHrExJIHoyZIrw"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    result = []
    for dics in json.loads(response.text)['results'] :
        result.append((dics['formatted_address'], dics['name'], dics['rating']))

    #Sort tuple based on rating in reverse order :
    result = sorted(result, key = lambda x: x[2], reverse=True)

    print(sortedLocs)
    countlist = []
    for ind in range(count):
       countlist.append(ind+1) 


    #Get distance and duration for city
    distance = Temp_info_1.objects.get(city=location).distance
    time = Temp_info_1.objects.get(city=location).time

    return render(request, 'output.html', {'sortedloc' : sortedloc[2:], 'countlist':countlist, 'location': sortedLocs[display + 1].capitalize(), 'result' : result, 'price':price, 'distance':distance, 'time':time})
    


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()


    def _returnCitiesUnderBudget(self,nodeid,budget):
        with self.driver.session() as session:
            result1 = session.read_transaction(self._returnCities,nodeid,budget)
            result2 = session.read_transaction(self._returnPrice,nodeid,budget)
            cities = []
            prices = []
            for row in result1:
                cities.append("{row}".format(row=row))

            for row in result2:
                prices.append("{row}".format(row=row))
            answer = []
            answer.append(cities)
            answer.append(prices)
            return answer

    @staticmethod
    def _returnCities(tx,nodeid,budget):
         query = (
            "MATCH (l:Loc) WHERE l.maxPrice <= {budget} AND l.parent_id={nodeid} RETURN l.name AS name".format(budget=budget, nodeid=nodeid)
        ) 
         result = tx.run(query, nodeid=nodeid,budget=budget)
         return [row["name"] for row in result]

    @staticmethod
    def _returnPrice(tx,nodeid,budget):
         query = (
            "MATCH (l:Loc) WHERE l.maxPrice <= {budget} AND l.parent_id={nodeid} RETURN l.maxPrice AS price".format(budget=budget, nodeid=nodeid)
        ) 
         result = tx.run(query, nodeid=nodeid,budget=budget)
         return [row["price"] for row in result]