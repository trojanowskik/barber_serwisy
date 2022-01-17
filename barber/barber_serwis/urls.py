from django.urls import path
from .views import BarberViewSet, LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, MakeSkills, SetSkills, SetVisit

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('view/', MakeSkills.as_view()),
    path('setskill/', SetSkills.as_view()),
    path('setvisit/', SetVisit.as_view()),
]
