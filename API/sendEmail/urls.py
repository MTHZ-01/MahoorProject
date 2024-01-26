from django.urls import path
from API.sendEmail.views import EmailAPIView

urlpatterns = [
    path('API/send_email/', EmailAPIView.as_view())
]
