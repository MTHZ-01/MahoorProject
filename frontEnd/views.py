from django.shortcuts import render, redirect
from frontEnd.models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, user_logged_in, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import requests
import numpy as np
import json

from storeBackEnd.settings import BASE_URL


def duplicateEliminator(lst):
    lstRefined = []
    for i in lst:
        if i not in lstRefined:
            lstRefined.append(i)
    return lstRefined


def getLogo(request):
    l = logo.objects.all()[0]

    return JsonResponse({"imgSrc": request.build_absolute_uri(l.logo.url)})


@csrf_exempt
def getProds(request):
    p = product.objects.all()
    s = Specs.objects.all()
    f = fetures.objects.all()
    d = division.objects.all()
    subD = division.objects.all()
    imgInline= prodImage.objects.all()
    # specifics = list(filter(lambda x : x.Prod.id == p[0].id, s))
    # s = map(lambda x: str(x), s)

    dataV2 = [
        {
            "title": p[i].title,
            "rawPrice": p[i].pricing,
            "price": (
                p[i].pricing * ((100 - p[i].discount) / 100)
                if p[i].discount != 0
                else p[i].pricing
            ),
            "discount": p[i].discount,
            "introduction": p[i].introduction,
            "imgUrl": list(map(lambda x: request.build_absolute_uri(x.img.url), filter(lambda x: x.p.id == p[i].id, imgInline)))[0] if len(list(map(lambda x: request.build_absolute_uri(x.img.url), filter(lambda x: x.p.id == p[i].id, imgInline)))) != 0 else "",
            "prodImgUrl": list(map(lambda x: request.build_absolute_uri(x.img.url), filter(lambda x: x.p.id == p[i].id, imgInline))),
            "features": list(
                map(lambda x: str(x), filter(lambda x: x.Prod.id == p[i].id, f))
            ),
            "specifics": list(
                map(lambda x: str(x), filter(lambda x: x.Prod.id == p[i].id, s))
            ),
            "divisions": p[i].division.name,
            "subDivisions": str(p[i].subDivision),
            "djangoId": p[i].id,
        }
        for i in range(len(p))
    ]

    return JsonResponse({"ProductData": dataV2})


def getDivisions(request):
    d = division.objects.all()

    data = [str(i) for i in d]

    return JsonResponse({"status": 200, "data": data})


def getDivisionsWithImg(request):
    d = division.objects.all()

    data = [
        {"name": str(i), "imgUrl": request.build_absolute_uri(i.img.url)} for i in d
    ]

    return JsonResponse({"status": 200, "data": data})


@csrf_exempt
def getSlider(request):
    s = Slider.objects.all()

    return JsonResponse(
        {
            "status": "success",
            "data": [
                {
                    "img": request.build_absolute_uri(i.img.url),
                    "route": f"category/{i.category}"
                    if i.category != None
                    else f"products/{i.Prod.title}",
                }
                for i in s
            ],
        }
    )


@csrf_exempt
def searchProds(request):
    searchQuerry = ""

    if request.GET.get("searchQuerry"):
        searchQuerry = request.GET.get("searchQuerry")

    if searchQuerry == "":
        return JsonResponse({"status": "url_Err"})

    p = product.objects.filter(title__icontains=searchQuerry)
    f = fetures.objects.all()
    s = Specs.objects.all()
    imgInline= prodImage.objects.all()
    dataV2 = [
        {
            "title": p[i].title,
            "price": p[i].pricing,
            "introduction": p[i].introduction,
            "imgUrl": list(map(lambda x: request.build_absolute_uri(x.img.url), filter(lambda x: x.p.id == p[i].id, imgInline)))[0] if len(list(map(lambda x: request.build_absolute_uri(x.img.url), filter(lambda x: x.p.id == p[i].id, imgInline)))) != 0 else "",

            "features": list(
                map(lambda x: str(x), filter(lambda x: x.Prod.id == p[i].id, f))
            ),
            "specifics": list(
                map(lambda x: str(x), filter(lambda x: x.Prod.id == p[i].id, s))
            ),
            "divisions": p[i].division.name,
            "djangoId": p[i].id,
        }
        for i in range(len(p))
    ]

    return JsonResponse({"Value": dataV2})


@csrf_exempt
def getAddress(request):
    options = json.loads(request.body)

    url = (
        f"https://api.neshan.org/v5/reverse?lat={options['lat']}&lng={options['longt']}"
    )

    info = requests.get(
        url,
        headers={
            "Api-Key": "service.b97f16d6446a41a19f13523dd5bdf6c2",
        },
    )
    info = info.json()

    return JsonResponse({"data": info})


@csrf_exempt
def searchLocations(request):
    body = json.loads(request.body)

    info = requests.get(
        f"https://api.neshan.org/v1/search?term={body['querry']}&lat={body['center']['latitude']}&lng={body['center']['longitude']}",
        headers={
            "Api-Key": "service.b97f16d6446a41a19f13523dd5bdf6c2",
        },
    )

    info = info.json()

    return JsonResponse({"locations": info})


@csrf_exempt
def getDivisionRelevency(request):
    d = json.loads(request.body)

    subD = subDivision.objects.all()

    p = product.objects.all()

    divisedProds = list(
        filter(
            lambda x: str(x.division) == d["divisionName"]
            and str(x.subDivision) != "None",
            p,
        )
    )

    if len(divisedProds) == 0:
        return JsonResponse({"data": []})
    else:
        return JsonResponse(
            {
                "data": duplicateEliminator(
                    list(map(lambda x: x.subDivision.name, divisedProds))
                )
            }
        )


@csrf_exempt
def getCity(request):
    try:
        states = requests.get("https://app.krch.ir/v1/get_state").json()["objects"]["state"]
        cities = requests.get("https://app.krch.ir/v1/get_city").json()["objects"]["city"]

        cityStates = []

        for city in cities:
            for state in states:
                if city["state_no"] == state["no"]:
                    cityStates.append(
                        {
                            "label": f"استان {state['name']} شهر {city['name']}",
                            "id": city["no"],
                        }
                    )
                    break

        return JsonResponse({"states": cityStates})
    except:
        return JsonResponse({"error": 199})


# @login_required(login_url=("Login"))
@csrf_exempt
def submitBuy(request):
    try:
        data = json.loads(request.body)

        # print(data)
        
        userId = data["userId"]
        cityId = data["cityId"]
        postalCode = data["postalCode"]
        address = data["address"]
        prodsInOrder = data["prodsInOrder"]
        # totalFee = data["totalFee"]

        # print(type(prodsInOrder))

        u = User.objects.get(id=userId)

        p = list(filter(lambda x: x.user.id == userId, list(profile.objects.all())))[0]

        o = Ord.objects.create(
            user=u,
            cityId=f"آدرس: {address}",
            postalCode=postalCode,
            cityAndStateName= f"استان و شهر: {cityId['label']}"  ,
            status="p",
        )

        go = giveOrd.objects.create(order=o, profile=p)
        # creating producs in the order list:
        for prod in prodsInOrder:
            djangoId = prod["djangoId"]
            rawProduct = product.objects.get(id=djangoId)
            newProdOrder = productsInOrder.objects.create(
                prod=rawProduct,
                order=o,
                explainations=prod["description"],
                width=prod["width"],
                height=prod["height"],
                chainPosition=prod["chainPosition"],
                installationPosition=prod["installationPosition"],
            )
            prodToAdd = product.objects.get(id=prod["djangoId"])
            pTop = prodToProfwhore.objects.create(prof=p, prod=prodToAdd)
            pTop.save()

        print(p)

        return JsonResponse({"status": 200})
    except Exception as e :
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {e}")
        return JsonResponse({"status": 199})


@csrf_exempt
def Login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data["username"]
        password = data["password"]

        try:
            user = User.objects.get(username=username)
            # if user.is_authenticated:
            # return JsonResponse({"status": 201 , "sessionId": user.id})

        except Exception as e:
            return JsonResponse({"status": 199 })


        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            return JsonResponse({"status": 200, "sessionId": user.id})

        return JsonResponse({"status": 199 })

    user = User.objects.get(username=username)

    if user.is_authenticated:
        return JsonResponse({"status": 201})
    else:
        return JsonResponse({"status": 199})


@csrf_exempt
def LogOut(request):
    logout(request)
    return JsonResponse({"status": 200})


@csrf_exempt
def registerUser(request):
    data = json.loads(request.body)
    username = data["mobile"]
    password = data["password"]

    try:
        u = User.objects.create(username=username, password=password)
        p = profile.objects.create(
            user=u,
            firstName=data["firstname"],
            lastName=data["lastname"],
            mobile=data["mobile"],
        )
        return JsonResponse({"status": 200})
    except Exception as e:
        return JsonResponse({"status": "DUP"})


@csrf_exempt
def getAllUserInfo(request):
    userId = json.loads(request.body)["userId"]

    p = profile.objects.get(id=userId)
    o = list(filter(lambda x: x.user.id == userId, Ord.objects.all()))
    o = list(filter(lambda x: x.status != "C", o))
    # o2 = list(Ord.objects.all())

    o = map(lambda x: x.dataOut(), o)

    jsonOutPut = p.dataOut()

    return JsonResponse({**jsonOutPut, "ords": list(o)})


@csrf_exempt
def delOrd(request):
    try:
        data = json.loads(request.body)

        ordId = data["ordId"]

        o = Ord.objects.get(id=ordId)

        o.status = "C"

        o.save()

        return JsonResponse({"status": 200})
    except:
        return JsonResponse({"status": "ERR"})


@csrf_exempt
def submitAComment(request):
    data = json.loads(request.body)

    try:
        p = profile.objects.get(id=data["id"])
        prod = product.objects.get(id=data["prodId"])
        prodToProf = prodToProfwhore.objects.all()
        prodToProf = list(filter(lambda x: x.prof.user.id == p.user.id, prodToProf))
        prodToProf = list(map(lambda x: x.prod.id, prodToProf))

        print(prod.id)
        if prod.id in prodToProf:
            c = comment.objects.create(author=p, message=data["message"], product=prod)

            print("succeed !!!")
            return JsonResponse({"status": 200})

    except Exception as e:
        print("Exceprion Happened", e)
        return JsonResponse({"status": str(e)})
    


    print(199)
    return JsonResponse({"status": 199})


@csrf_exempt
def getComments(request):
    try:
        data = json.loads(request.body)
        print(data["djangoId"])
        c = list(
            filter(
                lambda x: x.product.id == data["djangoId"], list(comment.objects.all())
            )
        )
        return JsonResponse(
            {"status": 200, "data": list(map(lambda x: x.giveData(), c))}
        )

    except Exception as e:
        return JsonResponse({"status": 199, "err": str(e)})


@csrf_exempt
def getMainMenu_first(request):
    obj = mainTableFirstPic.objects.all()[0]
    return JsonResponse(
        {
            "status": 200,
            "imgUrl": request.build_absolute_uri(obj.image.url),
            "division": str(obj.div),
            "subDivision": str(obj.subDiv),
            "prod": str(obj.prod),
        }
    )


@csrf_exempt
def getMainMenu_Second(request):
    obj = mainSecond.objects.all()


    return JsonResponse({"data": [

        {
            
            "imgUrl": request.build_absolute_uri(i.image.url),
            "division": str(i.div),
            "subDivision": str(i.subDiv),
            "prod": str(i.prod),
        }
    for i in obj ] ,"status": 200}
    )

@csrf_exempt
def getMainMenu_Third(request):
    obj = mainThird.objects.all()


    return JsonResponse({"data": [

        {
            
            "imgUrl": request.build_absolute_uri(i.image.url),
            "division": str(i.div),
            "subDivision": str(i.subDiv),
            "prod": str(i.prod),
        }
    for i in obj ] ,"status": 200}
    )



@csrf_exempt
def getSubDivisions(request):
    d = list(subDivision.objects.all())

    print(f"data data data data data data {[i.name for i in d]}")

    return JsonResponse({"status": 200 , "data": [i.name for i in d] })




@csrf_exempt
def chaparOrder(request):
    data = json.loads(request.body)
    

    url = "https://app.krch.ir/v1/bulk_import"

    actual = {
               

        "user": {
            "username": "behsaye",
            "password": "66085"
        },
        "bulk": [{
            "cn": {
                "reference": 123,
                "date": "2019-05-13",
                "assinged_pieces": data["pieces"],
                "service": "1",
                "value": data["price"],
                "payment_term": 0,
                "weight": "1",
                        "content":"شیشه و سنگ"
            },
            "sender": {
                "person": "ماهور",
                "company": "پرده ماهور",
                "city_no": "10866",
                "telephone": "+9888288475",
                "mobile": "989123181638",
                "email": "sender@test.com",
                "address": "آزمایشی فرستنده",
                "postcode": "10770"
            },
            "receiver": {
                "person": "آزمایشی گیرنده",
                "company": "شرکت گیرنده",
                "city_no": "10770",
                "telephone": "+9888269464",
                "mobile": "989034538660",
                "email": "test@test.com",
                "address": "آزمایشی گیرنده",
                "postcode": "10770"
            }
        }]
    }


    payload = {'input': f'''{str(actual)}'''}
    files=[

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)



@csrf_exempt
def getChaparPrice(request):
    data = json.loads(request.body)


    dest = data["dest"]
    value = data["value"]
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{dest}")
    actual =  {
    "order":{
        "origin":"10925",
        "destination":dest,
        "method":"11",
        "value":value,
        "weight":"4"
    }
    }

    url = "https://api.krch.ir/v1/get_quote"

    payload = {'input': f'{json.dumps(actual)}'}
    files=[

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print("trying")
    print(response.text)
    print(type(response.text))

    out = json.loads(response.text)
    print(out)



    return(JsonResponse({"status": 200, "data":str(int(out["objects"]["order"]["price"]["fld_Total_Cost"])/10) }))

@csrf_exempt
def handler404(request, exception):
    return redirect('https://pardehmahoor.ir/404')
    return JsonResponse({"Srt":200})
