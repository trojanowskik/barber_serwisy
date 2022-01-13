from django.urls import path
from .views import BarberViewSet, ClientViewSet, LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]
