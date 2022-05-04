from django.shortcuts import render
from requests.sessions import Request
import requests

# Create your views here.

endpoint = 'http://127.0.0.1:5000/' 
def home(request):
    response = requests.get(endpoint + 'show')
    analisis = response.json()
    context ={

    }
    return render(request, 'index.html', context)