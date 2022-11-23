from django.shortcuts import render
from functools import reduce
from operator import truediv
import os
from django.http import HttpResponse
import urllib
from elancoproject.settings import BASE_DIR
import requests
from .models import ElancoData
import json
# Create your views here.
#Homepage
def homepage(request):
    data = ElancoData.objects
    return render(request, 'home.html',{'data':data})

#Puts all the data from API to the model
def store_data(request):
    jsondata = get_data('https://engineering-task.elancoapps.com/api/raw')
    ElancoData.objects.all().delete()
    for i in jsondata:
        Elanco = ElancoData()
        Elanco.ConsumedQuantity = i["ConsumedQuantity"]
        Elanco.Cost = i["Cost"]
        Elanco.Date = dateformatter(i["Date"])
        Elanco.InstanceId = i["InstanceId"]
        Elanco.Location = i["Location"]
        Elanco.MeterCategory = i["MeterCategory"]
        Elanco.ResourceGroup = i["ResourceGroup"]
        Elanco.ResourceLocation = i["ResourceLocation"]
        Elanco.ServiceName = i["ServiceName"]
        Elanco.UnitOfMeasure = i["UnitOfMeasure"]
        Elanco.Tags = i["Tags"]
        Elanco.save()
    print("Done storing")
    return HttpResponse("Done")

#Gets the data from JSON url
def get_data(testurl):
    if (url := checkurl(testurl)):
        text = requests.get(url).text
        data = json.loads(text)
        return data
    else:
        response = HttpResponse()
        response.status_code = 404
        
#Checks if url is valid
def checkurl(url):
    req = requests.get(url)
    if (req.status_code == 200):
        return url
    else:
        return False

#Formatting date for model
def dateformatter(date):
    dlist = date.split("/")
    return dlist[2]+"-"+dlist[1]+"-"+dlist[0] 
