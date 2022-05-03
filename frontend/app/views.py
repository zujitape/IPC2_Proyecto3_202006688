from django.shortcuts import render
import requests

# Create your views here.
endpoint = 'http://127.0.0.1:5000/'
def home(request):
    response = requests.get(endpoint + 'add')

