from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json

def index(request):
    return render(request, 'index.html')

def proxy(request):
    json_data = json.dumps(request['urls'])
    r = requests.post('http://ec2-54-215-220-149.us-west-1.compute.amazonaws.com:8080/predict', json=json_data)
    return render(request, 'index.html')