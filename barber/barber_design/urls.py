from django.conf.urls import include
from django.urls import path
from .views import user_view, get_skills_view, create_skill, delete_skill, create_visit, get_visits_view, delete_visit, register_view, login_view

urlpatterns = [
    path('user/', user_view, name = 'user_view'),
    path('skills/', get_skills_view, name = 'skills_list'),
    path('create_skill/', create_skill, name = 'create_skill'),
    path('delete_skill/<int:id>', delete_skill, name = 'delete_skill'),
    path('create_visit/', create_visit, name = 'create_visit'),
    path('visits/', get_visits_view, name = 'visits_list'),
    path('delete_visit/<int:id>', delete_visit, name = 'delete_visit'),
    path('register/', register_view, name = 'register_view'),
    path('login/', login_view, name = 'login_view'),
]