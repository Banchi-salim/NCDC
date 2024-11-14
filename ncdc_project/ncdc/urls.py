from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('deparments', views.deparments, name='departments'),
    path('leadership/', views.leadership, name='leadership'),  # Add this if needed
    path('office-of-the-dg/', views.office_of_dg, name='office_of_dg'),
]
