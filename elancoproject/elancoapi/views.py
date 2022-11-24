from django.shortcuts import render
from functools import reduce
from operator import truediv
import os
from django.http import HttpResponse
import urllib
from elancoproject.settings import BASE_DIR
import requests
from .models import ElancoData, Resources
import json
# Create your views here.
#Homepage
def homepage(request):
    data = Resources.objects
    return render(request, 'home.html',{'data':data})
#-------------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------
#getting the list for homepage
def store_resources(request):
    testurl = "https://engineering-task.elancoapps.com/api/resources"
    if (url := checkurl(testurl)):
        retarr = []
        text = requests.get(url).text
        data = strToList(text)
        Resources.objects.all().delete()
        for i in data:
            resource = Resources()
            url_parts = ["https://engineering-task.elancoapps.com/api/resources/",i.replace(" ","%20")]
            resource.name = i
            resource.apiurl = reduce(urllib.parse.urljoin, url_parts)
            resource.save()
        print("Loaded Resources")

def strToList(text):
    textn=''
    for i in range (1,len(text)-2):
        if text[i].isalnum() or text[i] == "," or text[i]==' ':
            textn+=text[i]
    return textn.split(',')

#-----------------------------------------------------------------------------------------------------
def datapage(request):
    name = request.GET.get('name')
    print(name)
    data = ElancoData.objects.filter(ServiceName__icontains=name)
    print(data,"####")
    return render(request,"data.html",{"data":data})
