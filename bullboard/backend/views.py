from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

# *args lets us pass a number of arguments into the function
# **kwargs sends a dictionary w/ values associated with those arguments
def login_view(*args, **kwargs):
    # Return a basic home page response from the server
    return HttpResponse("<h1> This is where the login page will be. </h1>")


# this is just a test function
def another_view(*args, **kwargs):
    return HttpResponse("<h1> This is just a test for another page. </h1>")
