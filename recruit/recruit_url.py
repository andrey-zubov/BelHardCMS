from django.urls import path
from . import views


urlpatterns = [
    path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    path('base_of_clients/', views.base_of_clients, name='base_of_clients'),

]