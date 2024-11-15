from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('deparments', views.deparments, name='departments'),
    path('leadership', views.heads_of_departments, name='leadership'),  # Add this if needed
    path('dg/', views.office_of_dg, name='office_of_dg'),
]
