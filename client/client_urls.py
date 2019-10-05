from django.contrib.auth.decorators import login_required
from django.urls import path

from client import views
from client.views import OpinionDelete, FormEducation

urlpatterns = [
    path('', views.client_main_page, name='client'),  # main client page
    path('profile', views.client_profile, name='client_profile'),
    path('edit', views.client_edit_main, name='client_edit'),
    path('edit/skills', views.client_edit_skills, name='client_edit_skills'),
    path('edit/photo', views.client_edit_photo, name='client_edit_photo'),
    path('edit/cv', views.client_edit_cv, name='client_edit_cv'),
    path('edit/education', views.client_edit_education, name='client_edit_education'),
    path('edit/experience', views.client_edit_experience, name='client_edit_experience'),
    path('chat', login_required(views.MessagesView.as_view()), name='contact_with_centre'),

    
    ##Poland urls
    path('resumes/', resumes_list, name='resumes_list_url'),
    path('resumes/<str:slug>/', resume_detail, name='resume_detail_url'),
    path('resumes/<str:slug>/accepted_vacancies/', accepted_vacancies, name='accepted_vacancies_url'),
    path('resumes/<str:slug>/rejected_vacancies/', rejected_vacancies, name='rejected_vacancies_url'),
    path('resumes/<str:slug>/vacancies/', vacancies_list, name='vacancies_list_url'),
    path('resumes/vacancy/<str:slug>/', vacancy_detail, name='vacancy_detail_url'),
    path('accept_reject/', views.accept_reject),
    path('help/', help_list, name='help_list_url'),
    path('settings/', settings_list, name='settings_list_url'),
    path('on_off/', views.on_off),    # on_off settings for notifications
    path('viewed/', views.viewed),

    path(r'opinion/', views.opinion_list, name='opinion_list'),
    path(r'opinion/create/', views.OpinionCreate.as_view(), name='opinion_create'),
    path(r'opinion/<int:pk>/', views.opinion_detail, name='opinion_detail'),
    path(r'opinion/edit/<int:pk>/', views.answer_create, name='opinion_answer'),
    path(r'opinion/edit/<int:pk>/delete/', OpinionDelete.as_view(), name='opinion_delete'),
    path('login/', views.client_login),
    path('logout/', views.client_logout),
    path('tasks/', views.tasks, name='tasks_list'),
    path('edit/form_edu', FormEducation.as_view(), name='form_edu'),

]
