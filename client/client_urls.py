from django.contrib.auth.decorators import login_required
from django.urls import path

from client import views
from client.edit.load_data_list import (SkillsDataList, InstitutionDataList, CvPositionDataList)
from client.views import *

urlpatterns = [
    path('', views.client_main_page, name='client'),  # main client page
    path('profile', views.client_profile, name='client_profile'),

    # Team Rome (start) - Edit Forms URLs
    path('edit', views.ClientEditMain.as_view(), name='client_edit'),
    path('edit/skills', views.ClientEditSkills.as_view(), name='client_edit_skills'),
    path('edit/photo', views.ClientEditPhoto.as_view(), name='client_edit_photo'),
    path('edit/cv', views.ClientEditCv.as_view(), name='client_edit_cv'),
    path('edit/education', views.ClientEditEducation.as_view(), name='client_edit_education'),
    path('edit/experience', views.ClientEditExperience.as_view(), name='client_edit_experience'),
    path('edit/form_edu/', views.FormEducation.as_view(), name='form_edu'),
    path('edit/skills_data_list/', SkillsDataList.as_view(), name='skills_data_list'),
    path('edit/institution_data_list/', InstitutionDataList.as_view(), name='institution_data_list'),
    path('edit/cv_position_data_list/', CvPositionDataList.as_view(), name='cv_position_data_list'),
    # Team Rome (end)

    path('chat/', login_required(views.MessagesView.as_view()), name='contact_with_centre'),
    path(r'opinion/', opinion_list, name='opinion_list'),
    path(r'opinion/create/', OpinionCreate.as_view(), name='opinion_create'),
    path(r'opinion/<int:pk>/', opinion_detail, name='opinion_detail'),
    path(r'opinion/edit/<int:pk>/', answer_create, name='opinion_answer'),
    path(r'opinion/edit/<int:pk>/delete/', OpinionDelete.as_view(), name='opinion_delete'),
    path('login/', client_login),
    path('logout/', client_logout),
    path('tasks/', tasks, name='tasks_list'),

    # path('edit/form_edu/', views.form_education, name='form_edu'),
    path(r'checktask/', views.checktask),
    path(r'checknotifications/', views.checknotifications),
    path(r'settings/', views.settings_menu, name='settings_menu'),
    path(r'settingsset/', views.set_settings, name='settings_set'),

    
    ##Poland urls
    path('resumes/', resumes_list, name='resumes_list_url'),
    path('resumes/<id>/', resume_detail, name='resume_detail_url'),
    path('resumes/<id>/accepted_vacancies/', accepted_vacancies, name='accepted_vacancies_url'),
    path('resumes/<id>/rejected_vacancies/', rejected_vacancies, name='rejected_vacancies_url'),
    path('resumes/<id>/vacancies/', vacancies_list, name='vacancies_list_url'),
    path('resumes/vacancy/<id>/', vacancy_detail, name='vacancy_detail_url'),
    path('accept_reject/', views.accept_reject),
    path('help/', help_list, name='help_list_url'),
    path('settings/', settings_list, name='settings_list_url'),
    path('on_off/', views.on_off),    # on_off settings for notifications
    path('viewed/', views.viewed),

]
