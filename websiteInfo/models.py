from django.db import models

# Create your models here.



class address(models.Model):

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس"
    text = models.CharField(max_length=5000)

    def giveDataOut(self):
        return self.text
        

class accessInfo(models.Model):
    class Meta:
        verbose_name = "اطلاعات تماس:"
        verbose_name_plural = "اطلاعات تماس:"

    def __str__(self) -> str:
        return f"مدل شماره ی {self.id} "

class dataToAccess(models.Model):
    class Meta:
        verbose_name = "اطلاعاتی که میخواهید در پایین سایت نمایش دهید:"
        verbose_name_plural = "اطلاعاتی که میخواهید در پایین سایت نمایش دهید:"
    d= models.ForeignKey("accessInfo", on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=50, verbose_name="عنوان")
    value = models.CharField(max_length=50, verbose_name="مقدار")

    def __str__(self) -> str:
        return f"-------عنوان این مدل: {self.title}--------"

    def giveDataOut(self):
        return {
            "title": self.title,
            "value": self.value
        }

class description(models.Model):
    class Meta:
        verbose_name = "توضیحاتی که می خواهید در پایین سایت نمایش دهید:"
        verbose_name_plural = "توضیحاتی که می خواهید در پایین سایت نمایش دهید:"
    text = models.CharField(max_length=5000)


class aboutUs(models.Model):
    class Meta:

        verbose_name = "بخش درباره ی ما"
        verbose_name_plural = "بخش درباره ی ما"

    title= models.CharField(max_length=200, verbose_name="تایتل درباره ی ما", null=True, blank=True)
    content= models.CharField(max_length=2000, verbose_name="محتوای درباره ی ما", null=True, blank=True)

        