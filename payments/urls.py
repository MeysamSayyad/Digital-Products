from django.urls import path
from .views import PaymentView, GatewayView

urlpatterns = [
    path("payment/", PaymentView.as_view()),
    path("gateways/", GatewayView.as_view()),
]
