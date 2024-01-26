@csrf_exempt
def submitBuy(request):
    data = json.loads(request.body)

    # print(data)

    userId = data["userId"]
    cityId = data["cityId"]
    postalCode = data["postalCode"]
    address = data["address"]
    prodsInOrder = data["prodsInOrder"]
    totalFee = data["totalFee"]

    # print(type(prodsInOrder))

    u = User.objects.get(id=userId)

    p = list(filter(lambda x: x.user.id == userId, list(profile.objects.all())))[0]

    o = Ord.objects.create(
        user=u,
        cityId=cityId,
        postalCode=postalCode,
        cityAndStateName=address,
        status="p",
    )

    content = []

    go = giveOrd.objects.create(order=o, profile=p)
    # creating producs in the order list:
    for prod in prodsInOrder:
        lines = []

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

        lines.append("شناسه سفارش:" + f" {o.id}")
        lines.append("شناسه محصول:" + f" {rawProduct.id}")
        lines.append("نام محصول:" + f" {rawProduct.title}")

        if newProdOrder.explainations:
            lines.append("توضیحات تکمیلی:\n" + newProdOrder.explainations)

        lines.append("عرض:" + f" {newProdOrder.width}")
        lines.append("ارتفاع:" + f" {newProdOrder.height}")
        lines.append("محل زنجیر:" + f" {newProdOrder.chainPosition}")
        lines.append("محل نصب:" + f" {newProdOrder.installationPosition}")

        content.append("\n".join(lines))

        prodToAdd = product.objects.get(id=prod["djangoId"])
        pTop = prodToProfwhore.objects.create(prof=p, prod=prodToAdd)
        pTop.save()

    print(p)

    '''
    SEND EMAIL THROUGH API
    WHERE BASE_URL IS THE WEBSITES ADDRESS!!!
    '''
    email_content = {"subject":"سفارشات جدید!", "message": "\n\n".join(content)}
    requests.post(f"{BASE_URL}/API/send_email/", email_content)

    return JsonResponse({"status": 200})

