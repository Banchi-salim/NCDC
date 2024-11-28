from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("chatbot-api/", views.chatbot_api, name="chatbot_api"),
    path('about', views.about, name='about'),
    path('deparments', views.deparments, name='departments'),
    path('leadership', views.heads_of_departments, name='leadership'),
    path('dg/', views.office_of_dg, name='office_of_dg'),
    path("update-location/", views.update_location, name="update_location"),
    path('donate/', views.donate_page, name='donate_page'),
    path('process-donation/', views.process_donation, name='process_donation'),
    path('weekly-epidemiological-reports/', views.weekly_reports, name='weekly_reports'),
    path('Situation-reports/', views.situation_report_list, name='situation_report_list'),
    path('situation-report/<int:report_id>/', views.situation_report_details, name='situation_report_details'),
    path('project-reports/', views.project_reports, name='project_reports'),
    path('annual-reports/', views.annual_reports, name='annual_reports'),
    path('guidelines/', views.guidelines_list, name='guidelines_list'),
    path('guidelines/<int:pk>/files/', views.guideline_files, name='guideline_files'),
    path('establishment-documents/', views.establishment_documents_list, name='establishment_documents_list'),
]
