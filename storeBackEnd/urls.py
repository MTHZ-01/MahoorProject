from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path 
from payment import views as pv
from websiteInfo import views as wv
from django.views.generic import TemplateView

handler404 = 'frontEnd.views.handler404'
urlpatterns = [
    
    path("", include("reactui.urls")),
    path("shoppingCart", include("reactui.urls")),
    path("shoppingCart/", include("reactui.urls")),
    path("paymentSuccess", include("reactui.urls")),
    path("account", include("reactui.urls")),
    path("SignUp", include("reactui.urls")),
    path("SignUp/", include("reactui.urls")),
    path("Login", include("reactui.urls")),
    path("Login/", include("reactui.urls")),
    path("404/", include("reactui.urls")),
    path("404", include("reactui.urls")),

    re_path(r'^products/(?P<event_name>[\w\s]+)', include("reactui.urls")),
    re_path(r'^products/(?P<event_name>[\w\s]+)/?', include("reactui.urls")),
# (?P<event_name>[\w\s]+)/?
    
    re_path(r'^category/(?P<event_name>[\w\s]+)/?', include("reactui.urls")),
    re_path(r'^category/(?P<event_name>[\w\s]+)', include("reactui.urls")),

    re_path(r'^category/همه/(?P<event_name>[\w\s]+)', include("reactui.urls")),
    re_path(r'^category/همه/(?P<event_name>[\w\s]+)/?', include("reactui.urls")),

    re_path(r'^callBack/(?P<event_name>[\w\s]+)', include("reactui.urls")),

    re_path(r'^callBack/200/(?P<event_name>[\w\s]+)', include("reactui.urls")),

    re_path(r'^callBack/101/(?P<event_name>[\w\s]+)', include("reactui.urls")),

    re_path(r'^callBack/199/(?P<event_name>[\w\s]+)', include("reactui.urls")),


    path('admin/', admin.site.urls), # admin site
    path('admin', admin.site.urls), # admin site

    path("digitalAssets/", include("frontEnd.urls")),
    path('pay', pv.pay, name='pay'),
    path('pay/', pv.pay, name='pay'),

    re_path(r'^verify/(?P<event_name>[\w\s]+)', pv.verify),
    re_path(r'^verify/(?P<event_name>[\w\s]+)/', pv.verify),
    re_path(r'^verify.', pv.verify),


    path('webInfo/', include("websiteInfo.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# settings.MEDIA_ROOT
