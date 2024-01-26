from django.contrib import admin

# Register your models here.
from frontEnd.models import *


class feturesInline(admin.StackedInline):
    model = fetures
    extra = 0


class specsInline(admin.StackedInline):
    model = Specs
    extra = 0

class imageInline(admin.StackedInline):
    model = prodImage
    extra = 0

class prodAdmin(admin.ModelAdmin):
    inlines = [feturesInline, specsInline, imageInline]


class prodInline(admin.StackedInline):
    model = product
    inlines = [feturesInline, specsInline]
    extra = 0


class divisionAdmin(admin.ModelAdmin):
    inlines = [prodInline]


class subDivisionAdmin(admin.ModelAdmin):
    inlines = [prodInline]


@admin.action(description="تغییر وضعیت به ارسال شده")
def resolve(modeladmin, request, queryset):
    queryset.update(status="F")


@admin.action(description="تغییر وضعیت به لغو شده")
def cancled(modeladmin, request, queryset):
    queryset.update(status="F")


class productsInOrderInline(admin.StackedInline):
    model = productsInOrder
    extra = 0


class OrdAdmin(admin.ModelAdmin):
    model = Ord

    list_display = ["user", "status"]
    inlines = [productsInOrderInline]
    ordering = ["user"]
    actions = [resolve]


class ordInline(admin.StackedInline):
    model = giveOrd
    extra = 0


class commentInline(admin.StackedInline):
    model = comment
    extra = 0


class prodInlineForProf(admin.StackedInline):
    verbose_name = "محصولات خریداری شده:"
    verbose_name_plural = "محصولات خریداری شده:"

    model = prodToProfwhore
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    inlines = [ordInline, commentInline, prodInlineForProf]
    model = profile
    pass


admin.site.register(logo)
admin.site.register(mainTableFirstPic)
admin.site.register(mainSecond)
admin.site.register(mainThird)
admin.site.register(division)
admin.site.register(Ord, OrdAdmin)
admin.site.register(profile, ProfileAdmin)
admin.site.register(subDivision)
admin.site.register(Slider)
admin.site.register(registeredUser)
admin.site.register(product, prodAdmin)
