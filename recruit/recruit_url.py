from django.urls import path
from . import views


urlpatterns = [
    path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    path('base_of_clients/', views.base_of_applicants, name='base_of_clients'),
    path('base_of_clients/<id_a>/', views.applicant, name='applicant_url'),
    path('base_of_clients/<id_a>/tasks/', views.applicant_tasks, name='applicant_tasks_url'),
    # path('uploading_files/', views.uploading_files),

]