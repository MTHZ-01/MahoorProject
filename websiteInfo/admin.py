from django.contrib import admin
from websiteInfo.models import *


# Register your models here.


class dataToAccessInline(admin.StackedInline):
    model = dataToAccess
    extra = 0

class accessInfoAdmin(admin.ModelAdmin):
    inlines = [dataToAccessInline]

admin.site.register(address)
admin.site.register(accessInfo, accessInfoAdmin)
admin.site.register(aboutUs)
admin.site.register(description)