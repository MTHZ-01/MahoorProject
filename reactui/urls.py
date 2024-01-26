from django.urls import path

from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path("", views.index, name=""),
    # path("/ShoppingCart", views.index, name=""),
    # path("/products/:id", views.index, name=""),
    
    
    
    path('', TemplateView.as_view(template_name="index.html")),
    # path('/ShoppingCart', TemplateView.as_view(template_name="index.html")),
    # path('products/:id', TemplateView.as_view(template_name="index.html")),
    
]