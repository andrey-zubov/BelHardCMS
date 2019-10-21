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
