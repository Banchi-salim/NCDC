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
    path('process-donation/', views.process_donation, name='process_donation')
]
