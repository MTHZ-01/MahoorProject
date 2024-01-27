from typing import Any
from django.db import models
from django import forms
from django.contrib.auth.models import User
import json

# Create your models here.


class logo(models.Model):
    class Meta:
        verbose_name = "لوگو"
        verbose_name_plural = "لوگو"

    logo = models.ImageField(upload_to="")


class division(models.Model):
    class Meta:
        verbose_name = "تقسیم بندی ها"
        verbose_name_plural = "تقسیم بندی ها"

    name = models.CharField(max_length=150, verbose_name="نام دسته بندی")
    img = models.ImageField(
        upload_to="", verbose_name="تصویر دسته بندی"
    )

    def __str__(self) -> str:
        return self.name


class subDivision(models.Model):
    class Meta:
        verbose_name = "زیر تقسیم بندی ها"
        verbose_name_plural = "زیر تقسیم بندی ها"

    name = models.CharField(max_length=150, verbose_name="نام زیر دسته بندی", null=True)

    def __str__(self) -> str:
        return self.name


class prodImage(models.Model):
    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصویر محصول"

    img = models.ImageField(
        upload_to="", verbose_name="تصویر محصول"
    )
    p = models.ForeignKey("product", on_delete=models.CASCADE, null=True)

class product(models.Model):
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصول"

    # img = models.ImageField(
    #     upload_to="", verbose_name="تصویر محصول"
    # )

    title = models.CharField(max_length=300, verbose_name="تایتل")
    pricing = models.IntegerField(verbose_name="قیمت")
    ProductCode = models.IntegerField(verbose_name="کد محصول")

    discount = models.IntegerField(verbose_name="میزان تخفیف %", default=0)

    introduction = models.CharField(
        max_length=1500, verbose_name="درباره محصول (بخش معرفی)"
    )
    division = models.ForeignKey(
        division,
        on_delete=models.CASCADE,
        verbose_name="یکی از تقسیم بندی ها رو انتخاب کنید",
    )
    subDivision = models.ForeignKey(
        subDivision,
        on_delete=models.CASCADE,
        verbose_name="(انتخابی) یکی از زیر تقسیم بندی ها رو انتخاب کنید",
        blank=True,
        null=True,
    )

    def giveDataOut(self):
        pI = prodImage.objects.all()
        specificI = ""
        try:
            specificI = list(map(lambda x : x.p.id == self.id ,list(pI)))[0].img.url
        except:
            pass

        return {
            "imgUrl": specificI,
            "title": self.title,
            "introduction": self.introduction,
            "pricing": self.pricing,
            "division": str(self.division),
            "subDivision": str(self.subDivision),
        }

    def __str__(self) -> str:
        return self.title


class fetures(models.Model):
    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "بخش ویژگی ها در صفحه محصول"

    Prod = models.ForeignKey(
        product,
        on_delete=models.CASCADE,
    )
    item = models.CharField(max_length=100, verbose_name="ویژگی")

    def __str__(self):
        return self.item


class Specs(models.Model):
    class Meta:
        verbose_name = "مشخصه"
        verbose_name_plural = "بخش مشخصات در صفحه محصول"

    Prod = models.ForeignKey(product, on_delete=models.CASCADE)
    item = models.CharField(max_length=100, verbose_name="مشخصه")

    def __str__(self):
        return self.item


class Slider(models.Model):
    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر"

    img = models.ImageField(
        upload_to="digitalAssets/frontEnd/images//", verbose_name="تصویر اسلایدر"
    )
    Prod = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        division, on_delete=models.CASCADE, null=True, blank=True
    )


class registeredUser(models.Model):
    userName = models.CharField(max_length=150, null=True)

    def __str__(self) -> str:
        return self.userName


STATUS_CHOICES = [
    ("p", "در حال ارسال"),
    ("F", "ارسال شده"),
    ("C", "لغو شده"),
]


class productsInOrder(models.Model):
    class Meta:
        verbose_name = "محصولات"
        verbose_name_plural = "اجزاء سبد خرید"

    prod = models.ForeignKey(product, on_delete=models.DO_NOTHING, null=True, verbose_name="نام محصول")
    order = models.ForeignKey("Ord", on_delete=models.CASCADE, null=True )
    width = models.IntegerField( verbose_name="طول")
    height = models.IntegerField( verbose_name="ارتفاع")
    explainations = models.CharField(max_length=1000, null=True, verbose_name="توضیحات مشتری درباره این مورد")
    chainPosition = models.CharField(max_length=1000, null=True, verbose_name="محل زنجیر")
    installationPosition = models.CharField(max_length=1000, null=True, verbose_name="محل نصب" )

    def giveDataOut(self):
        return {
            "prod": self.prod.giveDataOut(),
            "explainations": self.explainations,
            "chainPosition": self.chainPosition,
            "installationPosition": self.installationPosition,
        }


class Ord(models.Model):
    class Meta:
        verbose_name = "سفارشات"
        verbose_name_plural = "سفارشات"

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    cityId = models.CharField(max_length=10, null=True)
    cityAndStateName = models.CharField(max_length=1000, null=True)
    postalCode = models.CharField(max_length=10, null=True)
    # pInO = models.ForeignKey(productsInOrder, on_delete=models.PROTECT, null=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="p", verbose_name="وضعیت ارسال"
    )

    def dataOut(self) -> dict:
        prodsInOrder = list(
            filter(lambda x: x.order.id == self.id, productsInOrder.objects.all())
        )

        prodsInOrder = list(map(lambda x: x.giveDataOut(), prodsInOrder))
        statusValue = list(filter(lambda x: x[0] == self.status, STATUS_CHOICES))[0]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", type(statusValue))

        return {
            "cityId": self.cityId,
            "ordId": self.id,
            "status": self.status,
            "postalCode": self.postalCode,
            "address": self.cityAndStateName,
            "prodsInOrder": prodsInOrder,
            "status": statusValue[1],
            "cityAndStateName": self.cityAndStateName,
        }

    def __str__(self):
        return f"cityId: {self.cityId} status: {self.status} "


class giveOrd(models.Model):
    order = models.ForeignKey("Ord", on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(
        "profile", on_delete=models.PROTECT, null=True, blank=True
    )


class profile(models.Model):
    class Meta:
        verbose_name = "مشتریان احتمالی"
        verbose_name_plural = "مشتریان احتمالی"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstName = models.CharField(max_length=120, null=True, blank=True)
    lastName = models.CharField(max_length=120, null=True, blank=True)
    mobile = models.CharField(max_length=16, null=True, blank=True)

    def dataOut(self):
        return {
            "username": str(self.user),
            "firstname": self.firstName,
            "lastname": self.lastName,
            "mobile": self.mobile,
        }

    def __str__(self):
        return json.dumps(
            {
                "username": str(self.user),
                "firstname": self.firstName,
                "lastname": self.lastName,
                "mobile": self.mobile,
            }
        )


class prodToProfwhore(models.Model):
    class Meta:
        verbose_name = "محصولات خریداری شده:"
        verbose_name_plural = "محصولات خریداری شده:"

    prof = models.ForeignKey("profile", on_delete=models.CASCADE)
    prod = models.ForeignKey("product", on_delete=models.CASCADE)


class comment(models.Model):
    class Meta:
        verbose_name = "کامنت ها:"
        verbose_name_plural = "کامنت ها:"

    author = models.ForeignKey(profile, on_delete=models.PROTECT, null=True, blank=True)
    product = models.ForeignKey(
        product, on_delete=models.CASCADE, null=True, editable=False
    )
    message = models.CharField(
        max_length=800, verbose_name="کامنت", null=True, blank=True, editable=False
    )

    def __str__(self) -> str:
        return f"-نویسنده ی کامنت: {self.author.firstName} {self.author.lastName} \n -موبایل: {self.author.mobile} \n -کامنت: {self.message}"

    def giveData(self):
        return {
            "autuor": self.author.firstName + self.author.lastName,
            "productId": self.product.id,
            "message": self.message,
        }


class mainTableFirstPic(models.Model):
    class Meta:
        verbose_name = "تصویر اول منوی اصلی:"
        verbose_name_plural = "تصویر اول منوی اصلی:"

    image = models.ImageField(upload_to="")
    div = models.ForeignKey(
        division,
        on_delete=models.PROTECT,
        verbose_name="تقسیم بندی",
        null=True,
        blank=True,
    )
    subDiv = models.ForeignKey(
        subDivision,
        on_delete=models.PROTECT,
        verbose_name="زیر تقسیم بندی",
        null=True,
        blank=True,
    )
    prod = models.ForeignKey(
        product, on_delete=models.PROTECT, verbose_name="محصول", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk and mainTableFirstPic.objects.exists():
            # if you'll not check for self.pk
            # then error will also be raised in the update of exists model
            raise "There can only be one instance"
        return super(mainTableFirstPic, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return str(self.id)

class mainSecond(models.Model):
    class Meta:
        verbose_name = "تصاویر دوم منوی اصلی:"
        verbose_name_plural = "تصاویر دوم منوی اصلی:"

    image = models.ImageField(upload_to="")
    div = models.ForeignKey(
        division,
        on_delete=models.PROTECT,
        verbose_name="تقسیم بندی",
        null=True,
        blank=True,
    )
    subDiv = models.ForeignKey(
        subDivision,
        on_delete=models.PROTECT,
        verbose_name="زیر تقسیم بندی",
        null=True,
        blank=True,
    )
    prod = models.ForeignKey(
        product, on_delete=models.PROTECT, verbose_name="محصول", null=True, blank=True
    )


class mainThird(models.Model):
    class Meta:
        verbose_name = "تصویر سوم منوی اصلی:"
        verbose_name_plural = "تصویر سوم منوی اصلی:"

    image = models.ImageField(upload_to="")
    div = models.ForeignKey(
        division,
        on_delete=models.PROTECT,
        verbose_name="تقسیم بندی",
        null=True,
        blank=True,
    )
    subDiv = models.ForeignKey(
        subDivision,
        on_delete=models.PROTECT,
        verbose_name="زیر تقسیم بندی",
        null=True,
        blank=True,
    )
    prod = models.ForeignKey(
        product, on_delete=models.PROTECT, verbose_name="محصول", null=True, blank=True
    )


