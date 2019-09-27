from django.urls import path

from . import views

urlpatterns = [
    path('', views.client_main_page, name='client'),  # main client page
    path('profile', views.client_profile, name='client_profile'),
    path('edit', views.client_edit_main, name='client_edit'),
    path('edit/skills', views.client_edit_skills, name='client_edit_skills'),
    path('edit/photo', views.client_edit_photo, name='client_edit_photo'),
    path('edit/cv', views.client_edit_cv, name='client_edit_cv'),
    path('edit/education', views.client_edit_education, name='client_edit_education'),
    path('edit/experience', views.client_edit_experience, name='client_edit_experience'),
    path('edit/form_edu', views.form_education, name='form_edu'),
]
