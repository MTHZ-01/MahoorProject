from django.http import HttpResponse, JsonResponse

from django.shortcuts import redirect
from suds.client import Client
import json
from django.views.decorators.csrf import csrf_exempt

MERCHANT_ID = "6ef1a0b0-d5c8-4bc3-898b-2dbfe0627178"  # Required
ZARINPAL_WEBSERVICE = (
    "https://www.zarinpal.com/pg/services/WebGate/wsdl"  # Required
)
amount = 5000  # Amount will be based on Toman  Required
description = "پول وده, پول زور ورده"  # Required
email = "user@userurl.ir"  # Optional
mobile = "09123456789"  # Optional
CallbackURL = "http://127.0.0.1:8000/verify/"


@csrf_exempt
def pay(request):
    global amount
    data = json.loads(request.body)
    # MERCHANT_ID = data["MMERCHANT_ID"]
    amount = data["amount"]
    descriptionList = [data["description"][i]["title"]+ " " for i in range(len(data["description"]))]
    description = "" 
    # email = data["email"]
    # mobile = data["mobile"]
    # CallbackURL = data["CallbackURL"]
    for i in descriptionList: description+= i + " "
    print(description)

    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(
        MERCHANT_ID, amount, description, email, mobile, CallbackURL
    )
    if result.Status == 100:
        # return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + result.Authority)
        return JsonResponse(
            {
                "status": 200,
                "url": f"https://www.zarinpal.com/pg/StartPay/{result.Authority}",
                "auth": result.Authority,
            }
        )

    else:
        return JsonResponse({"status": 199})


@csrf_exempt
def verify(request):
    client = Client(ZARINPAL_WEBSERVICE)
    if request.GET.get("Status") == "OK":
        result = client.service.PaymentVerification(
            MERCHANT_ID, request.GET["Authority"], amount
        )

        print(f"{result.Status }&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        if result.Status == 100 or result.Status == 200 :
            # return HttpResponse(" تراکنش موفق شماره بیگیری:" + str(result.RefID))
            return redirect(f"http://127.0.0.1:8000/callBack/200/{str(result.RefID)}")
        elif result.Status == 101:
            return redirect(f"http://127.0.0.1:8000/callBack/101/nothing")
            # return HttpResponse("تراکنش ثبت شده است : " + str(result.Status))
        else:
            return redirect(f"http://127.0.0.1:8000/callBack/199/nothing")
            # return HttpResponse("Transaction failed. Status: " + str(result.Status))
    else:
        return redirect(f"http://127.0.0.1:8000/callBack/199/nothing")

