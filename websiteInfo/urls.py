from django.urls import path


from . import views

urlpatterns = [
    path("address", views.getAddress, name="address"),
    path("getAccessData", views.getAccessData, name="getAccessData"),
    path("getAboutInfo", views.getAboutInfo, name="getAboutInfo"),
]
