from django.urls import path
from .views import RegisterView, GetTokenView

urlpatterns = [
    path("register/", RegisterView.as_view()),
]
