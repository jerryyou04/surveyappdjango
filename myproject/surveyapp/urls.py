from django.urls import path
from . import views

app_name = 'surveyapp'

urlpatterns = [
    path('<int:survey_id>/', views.display_survey, name='display_survey'),
    path('success/', views.survey_success, name='survey_success'),
    path('', views.survey_list, name='survey_list'),  # List all surveys
]
