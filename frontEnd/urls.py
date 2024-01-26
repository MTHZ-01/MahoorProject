from django.urls import path


from . import views

urlpatterns = [
    path("logo", views.getLogo, name="logo"),
    path("prods", views.getProds, name="prods"),
    path("divisions", views.getDivisions, name="divisions"),
    path("divisionsImg", views.getDivisionsWithImg, name="divisionsImg"),
    path("slider", views.getSlider, name="slider"),
    path("search", views.searchProds, name="search"),
    path("getAddress", views.getAddress, name="getAddress"),
    path("searchPlace", views.searchLocations, name="searchPlace"),
    path("getDivRel", views.getDivisionRelevency, name="getDivRel"),
    path("getCity", views.getCity, name="getCity"),
    path("submitBuy", views.submitBuy, name="submitBuy"),
    path("Login", views.Login, name="Login"),
    path("LogOut", views.LogOut, name="LogOut"),
    path("registerUser", views.registerUser, name="registerUser"),
    path("getAllUserInfo", views.getAllUserInfo, name="getAllUserInfo"),
    path("deleteOrd", views.delOrd, name="deleteOrd"),
    path("submitAComment", views.submitAComment, name="submitAComment"),
    path("getComments", views.getComments, name="getComments"),
    path("getMainMenu_first", views.getMainMenu_first, name="getMainMenu_first"),
    path("getMainMenu_Second", views.getMainMenu_Second, name="getMainMenu_Second"),
    path("getMainMenu_Third", views.getMainMenu_Third, name="getMainMenu_Third"),
    path("getSubDivisions", views.getSubDivisions, name="getSubDivisions"),
    path("getChaparPrice", views.getChaparPrice, name="getChaparPrice"),
]
