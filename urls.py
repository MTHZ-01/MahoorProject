from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path 
from payment import views as pv
from websiteInfo import views as wv
from django.views.generic import TemplateView


urlpatterns = [
    
    path("", include("reactui.urls")),
    path("shoppingCart", include("reactui.urls")),
    path("paymentSuccess", include("reactui.urls")),
    path("account", include("reactui.urls")),
    path("SignUp", include("reactui.urls")),
    path("login", include("reactui.urls")),
    re_path(r'^products/(?P<word>\w+)', include("reactui.urls")),
    re_path(r'^category/(?P<word>\w+)', include("reactui.urls")),
    re_path(r'^callBack/(?P<word>\w+)', include("reactui.urls")),


    path('admin/', admin.site.urls), # admin site
    path("digitalAssets/", include("frontEnd.urls")),
    path('pay', pv.pay, name='pay'),
    re_path(r'^verify.*', pv.verify),
    path('webInfo/', include("websiteInfo.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# settings.MEDIA_ROOT
