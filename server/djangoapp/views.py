from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)
 


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if(request.method=='POST'):
        username= request.POST['username']
        password= request.POST['psw']
        user= authenticate(username= username, password= password)
        if user is not None:
            login(request,user)
            return redirect('djangoapp:index')
        else:
            return render(request,'djangoapp/login.html',context)
    else:
        return render(request,'djangoapp/login.html',context)



# Create a `logout_request` view to handle sign out request
def logout_request(request):
   # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    if request.method=='GET':
       return render(request,'djangoapp/registration.html', context)
    elif request.method=='POST':
        username= request.POST['username']
        password=request.POST['password']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        user_exist=False
        try:
            User.objects.get(username=username)
            user_exist=True
        except:
            logger.debug('{} user already exist'.format(username))
        if not user_exist:
            user= User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password= password)
            login(request,user)
            return redirect('djangoapp:index')
        else:
            return render(request,'djangoapp/registration.html', context)            





# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context=dict()
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/274a5e38-067d-4b29-9c70-80e084b095db/default/get_dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        
        context['dealership_list']=dealerships 
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context=dict()
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/274a5e38-067d-4b29-9c70-80e084b095db/default/get_dealerships"
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url)
        context['reviews_list']=dealer_reviews
        # Concat all dealer's short name
        reviews = ' '.join([rev.review for rev in dealer_reviews])
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # if request.method=='GET':
        
    if request.method=='POST':
        if User.is_authenticated:
            review=dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = 11
            review["review"] = "This is a great car dealer"
            json_payload=dict()
            json_payload["review"] = review
            response=post_request(url, json_payload, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)




    



