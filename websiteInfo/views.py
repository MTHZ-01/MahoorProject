from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

@csrf_exempt
def getAddress(request):
    a = list(address.objects.all())[-1]


    return JsonResponse({"status": 200 , "data": a.giveDataOut()})


@csrf_exempt
def getAccessData(request):
    a = list(accessInfo.objects.all())[-1]
    inlineAccess = dataToAccess.objects.all()

    inlineData = [i.giveDataOut() for i in inlineAccess if i.d.id == a.id]


    return JsonResponse({
        "status": 200,
        "data": inlineData
    })



@csrf_exempt
def getAboutInfo(request):
    a = list(aboutUs.objects.all())[-1]


    return(JsonResponse({"status":200 ,"title": a.title, "content": a.content }))